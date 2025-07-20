import streamlit as st
from server.stores.config_store import CONFIG_STORE
from frontend.state import create_llm_instance
from config import RESPONSE_MODE, DEFAULT_RESPONSE_MODE

st.header("系统设置")
advanced_settings = st.container(border=True)

if "response_mode" not in st.session_state:
    st.session_state["response_mode"] = st.session_state["current_llm_settings"].get("response_mode", DEFAULT_RESPONSE_MODE)

def change_top_k():
    st.session_state["current_llm_settings"]["top_k"] = st.session_state["top_k"]
    CONFIG_STORE.put(key="current_llm_settings", val=st.session_state["current_llm_settings"])
    create_llm_instance()

def change_temperature():
    st.session_state["current_llm_settings"]["temperature"] = st.session_state["temperature"]
    CONFIG_STORE.put(key="current_llm_settings", val=st.session_state["current_llm_settings"])
    create_llm_instance()

def change_system_prompt():
    st.session_state["current_llm_settings"]["system_prompt"] = st.session_state["system_prompt"]
    CONFIG_STORE.put(key="current_llm_settings", val=st.session_state["current_llm_settings"])
    create_llm_instance()

def change_response_mode():
    st.session_state["current_llm_settings"]["response_mode"] = st.session_state["response_mode"]
    CONFIG_STORE.put(key="current_llm_settings", val=st.session_state["current_llm_settings"])
    create_llm_instance()

with advanced_settings:
    col_1, _, col_2 = st.columns([4, 2, 4])
    with col_1:
        st.number_input(
            "多少个最相关的文档索引",
            min_value=1,
            max_value=100,
            help="响应查询而检索的最相似文档的数量。",
            value=st.session_state["current_llm_settings"]["top_k"],
            key="top_k",
            on_change=change_top_k,
        )
    with col_2:
        st.select_slider(
            "Temperature",
            options=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1],
            help="生成响应时使用的T。更高的T会导致更多的随机响应。(出现幻觉，建议谨慎，一般为0.3-0.7)",
            value=st.session_state["current_llm_settings"]["temperature"],
            key="temperature",
            on_change=change_temperature,
        )
    st.text_area(
        "System Prompt-系统提示词",
        help="生成响应时使用的提示。系统提示用于为模型提供上下文。",
        value=st.session_state["current_llm_settings"]["system_prompt"],
        key="system_prompt",
        height=240,
        on_change=change_system_prompt,
    )
    st.selectbox(
        "响应模式",
        options=RESPONSE_MODE,
        help="设置创建查询引擎时使用的Llama索引查询引擎响应模式。默认是: `simple_summarize`.",
        key="response_mode",
        # index=RESPONSE_MODE.index(st.session_state["current_llm_settings"]["response_mode"]), # simple_summarize by default
        on_change=change_response_mode,
    )

# For debug purpost only
def show_session_state():
    st.write("")
    with st.expander("List of current application parameters"):
        state = dict(sorted(st.session_state.items()))
        st.write(state)
