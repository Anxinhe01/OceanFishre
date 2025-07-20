import logging
import sys

from scipy._lib.array_api_compat import size

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

import streamlit as st
from frontend.state import init_state

if __name__ == '__main__':
    st.set_page_config(
        page_title="示例",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    st.logo("frontend/images/ThinkRAG_Logo.png",size="large")

    logo_path = "frontend/images/ThinkRAG_Logo.png"
    st.image(logo_path,width=125)

    init_state()

    pages = {
        "应用": [
            st.Page("frontend/Document_QA.py", title="提问主页"),
            st.Page("frontend/water_monitor.py", title="实时水质监控"),
        ],
        "RAG文件来源": [
            st.Page("frontend/KB_File.py", title="上传文件"),
            st.Page("frontend/KB_Manage.py", title="文件管理"),
        ],
        "模型与工具": [
            st.Page("frontend/Model_LLM.py", title="LLM"),
            st.Page("frontend/Model_Rerank.py", title="重排序"),
        ],
        "其它设置": [
            st.Page("frontend/Setting_Advanced.py", title="更多设置"),
        ],
    }


    pg = st.navigation(pages, position="sidebar")

    pg.run()

# ollama 0.3.3
# mysql.connector
# python-docx