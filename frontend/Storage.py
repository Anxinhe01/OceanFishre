import streamlit as st
from config import THINKRAG_ENV

st.header("存储")
st.caption("所有数据都存储在本地文件系统或配置的数据库中。",
           )

embedding_settings = st.container(border=True)
with embedding_settings:
    st.info("Running ThinkRAG in ‘ " + THINKRAG_ENV + " ’ mode.")
    st.dataframe(data={
        "存储类型": ["矢量", "文档", "索引", "对话", "配置"],
        "开发模式": ["Simple Vector Store", "Simple Document Store", "Simple Index Store",
                     "Simple Chat Store (in memory)", "Simple KV Store"],
        "产品": ["Chroma", "Redis", "Redis", "Redis", "Simple KV Store"],

    }, hide_index=True)
