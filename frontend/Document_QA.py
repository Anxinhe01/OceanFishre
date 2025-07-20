import time
import re
import streamlit as st
import pandas as pd
from vosk import SetLogLevel
import mysql.connector

from frontend.doc_saver import save_to_doc
from frontend.voice_input import SaveWave
from server.stores.chat_store import CHAT_MEMORY
from llama_index.core.llms import ChatMessage, MessageRole
from server.engine import create_query_engine
from server.stores.config_store import CONFIG_STORE


def get_latest_water_quality():
    conn = mysql.connector.connect(

    )
    c = conn.cursor()
    query = "SELECT * FROM water_quality ORDER BY id DESC LIMIT 1"
    c.execute(query)
    record = c.fetchone()
    conn.close()
    if record:
        return {
            'turbidity': record[1],
            'pH': record[2],
            'ammonia_nitrogen': record[3],
            'dissolved_oxygen': record[4]
        }
    else:
        return None


def perform_query(prompt):
    if not st.session_state.query_engine:
        print("Index is not initialized yet")
    if (not prompt) or prompt.strip() == "":
        print("Query text is required")

    # 检查提问内容是否涉及实时水质
    if "实时水质" in prompt or "水质监控" in prompt:
        latest_water_quality = get_latest_water_quality()
        if latest_water_quality:
            water_quality_info = (
                f"最新的水质信息如下："
                f"透明度: {latest_water_quality['turbidity']}, "
                f"pH: {latest_water_quality['pH']}, "
                f"氨氮含量: {latest_water_quality['ammonia_nitrogen']}, "
                f"溶解氧: {latest_water_quality['dissolved_oxygen']}。"
            )
            prompt += "\n\n" + water_quality_info

    try:
        query_response = st.session_state.query_engine.query(prompt)
        return query_response
    except Exception as e:
        print(f"An error occurred while processing the query: {type(e).__name__}: {e}")


def simple_format_response_and_sources(response):
    primary_response = getattr(response, 'response', '')
    output = {"response": primary_response}
    sources = []
    if hasattr(response, 'source_nodes'):
        for node in response.source_nodes:
            node_data = getattr(node, 'node', None)
            if node_data:
                metadata = getattr(node_data, 'metadata', {})
                text = getattr(node_data, 'text', '')
                text = re.sub(r'\n\n|\n|\u2028', lambda m: {'\n\n': '\u2028', '\n': ' ', '\u2028': '\n\n'}[m.group()],
                              text)
                source_info = {
                    "file": metadata.get('file_name', 'N/A'),
                    "page": metadata.get('page_label', 'N/A'),
                    "text": text
                }
                sources.append(source_info)
    output['sources'] = sources
    return output


def chatbox():
    # Load Q&A history
    messages = CHAT_MEMORY.get()
    if len(messages) == 0:
        # Initialize Q&A record
        CHAT_MEMORY.put(ChatMessage(role=MessageRole.ASSISTANT, content="这里是渔业GPT，在下面开始提问！"))  # 开场词
        messages = CHAT_MEMORY.get()

    # Show Q&A records
    for message in messages:
        with st.chat_message(message.role):
            st.write(message.content)

    voice_text = ""
    if st.session_state.get("voice_text"):
        voice_text = st.session_state.voice_text

    prompt = st.text_input("输入问题", value=voice_text)

    if st.button("提交问题") and prompt.strip():
        with st.chat_message(MessageRole.USER):
            st.write(prompt)
            CHAT_MEMORY.put(ChatMessage(role=MessageRole.USER, content=prompt))
            st.session_state.prompt = prompt

        with st.chat_message(MessageRole.ASSISTANT):
            with st.spinner("思考中..."):
                start_time = time.time()
                response = perform_query(prompt)
                end_time = time.time()
                query_time = round(end_time - start_time, 2)
                if response is None:
                    st.write("Couldn't come up with an answer.")
                else:
                    response_text = st.write_stream(response.response_gen)
                    st.session_state.response_text = response_text
                    st.write(f"Took {query_time} second(s)")
                    details_title = f"找到了 {len(response.source_nodes)} 个相关文件来源"
                    with st.expander(
                            details_title,
                            expanded=False,
                    ):
                        source_nodes = []
                        for item in response.source_nodes:
                            node = item.node
                            score = item.score
                            title = node.metadata.get('file_name', None)
                            if title is None:
                                title = node.metadata.get('title', 'N/A')
                                continue
                            page_label = node.metadata.get('page_label', 'N/A')
                            text = node.text
                            short_text = text[:50] + "..." if len(text) > 50 else text
                            source_nodes.append(
                                {"相关文件名称": title, "对应页码": page_label, "内容": short_text, "相关度（Score）": f"{score:.2f}"})
                        df = pd.DataFrame(source_nodes)
                        st.table(df)
                    # store the answer in the chat history
                    CHAT_MEMORY.put(ChatMessage(role=MessageRole.ASSISTANT, content=response_text))


def main():
    model_path = "vosk/vosk-model-small-cn-0.22"
    SetLogLevel(-1)

    if st.button("语音输入"):
        st.toast('开始语音输入！')
        voice_text = SaveWave(model_path)
        if voice_text:
            print(voice_text)
            st.success("识别结果： " + voice_text)
            st.session_state.voice_text = voice_text  # Save the recognized voice text to session state

    st.header("开始提问")
    if st.session_state.llm is not None:
        current_llm_info = CONFIG_STORE.get(key="current_llm_info")
        current_llm_settings = CONFIG_STORE.get(key="current_llm_settings")
        st.caption("目前的模型：`" + current_llm_info["service_provider"] + "` `" + current_llm_info["model"] +
                   "` 响应模式： `" + current_llm_settings["response_mode"] +
                   "` 最相关文件数：`" + str(current_llm_settings["top_k"]) +
                   "` Temperature `" + str(current_llm_settings["temperature"]) +
                   "` 是否重排序：`" + str(current_llm_settings["use_reranker"]) +
                   "`"
                   )
        if st.session_state.index_manager is not None:
            if st.session_state.index_manager.check_index_exists():
                st.session_state.index_manager.load_index()
                st.session_state.query_engine = create_query_engine(
                    index=st.session_state.index_manager.index,
                    use_reranker=current_llm_settings["use_reranker"],
                    response_mode=current_llm_settings["response_mode"],
                    top_k=current_llm_settings["top_k"],
                    top_n=current_llm_settings["top_n"],
                    reranker=current_llm_settings["reranker_model"])
                print("Index loaded and query engine created")
                chatbox()
                if ('报告' in st.session_state.get('prompt', '') or '报告' in st.session_state.get('response_text',
                                                                                                   '')) and st.button(
                        "保存到DOC"):
                    if 'response_text' in st.session_state:
                        print("回答内容：" + st.session_state.response_text)
                        save_to_doc(st.session_state.response_text)

            else:
                print("Index does not exist yet")
                st.warning("你的知识库是空的。请先上传一些文件到里面。")
        else:
            print("IndexManager is not initialized yet.")
            st.warning("Please upload documents into your knowledge base first.")
    else:
        st.warning("请先配置LLM。")


main()
