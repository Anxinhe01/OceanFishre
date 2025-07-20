import streamlit as st
from config import RERANKER_MODEL_PATH
from server.stores.config_store import CONFIG_STORE

st.header("模型重新排序")
st.caption("配置重新排序模型",
           help="重新排序是根据一组标准对项目列表进行重新排序的过程。在搜索引擎中，重新排序用于通过考虑有关被排序项目的其他信息来提高搜索结果的相关性。",
           )


def change_use_reranker():
    st.session_state["current_llm_settings"]["use_reranker"] = st.session_state["use_reranker"]
    CONFIG_STORE.put(key="current_llm_settings", val=st.session_state["current_llm_settings"])


def change_top_n():
    st.session_state["current_llm_settings"]["top_n"] = st.session_state["top_n"]
    CONFIG_STORE.put(key="current_llm_settings", val=st.session_state["current_llm_settings"])


def change_reranker_model():
    st.session_state["current_llm_settings"]["reranker_model"] = st.session_state["selected_reranker_model"]
    CONFIG_STORE.put(key="current_llm_settings", val=st.session_state["current_llm_settings"])


reranking_settings = st.container(border=True)
with reranking_settings:
    st.toggle("使用重新排序",
              key="use_reranker",
              value=st.session_state["current_llm_settings"]["use_reranker"],
              on_change=change_use_reranker,
              )
    if st.session_state["current_llm_settings"]["use_reranker"] == True:
        st.number_input(
            "Top N-相关文件个数",
            min_value=1,
            max_value=st.session_state["current_llm_settings"]["top_k"],
            help="响应查询而检索的最相似文档的数量。",
            value=st.session_state["current_llm_settings"]["top_n"],
            key="top_n",
            on_change=change_top_n,
        )

        reranker_model_list = list(RERANKER_MODEL_PATH.keys())
        reranker_model = st.selectbox(
            "选择重排序模型",
            reranker_model_list,
            key="selected_reranker_model",
            index=reranker_model_list.index(st.session_state["current_llm_settings"]["reranker_model"]),
            on_change=change_reranker_model,
        )

        st.caption(
            "可以在`config.py`文件中指定要使用的模型。")
        # st.caption(
        #     "It is recommended to download the models to the `localmodels` directory, in case you need run the system without an Internet connection. Plase refer to the instructions in `docs` directory.")
        #