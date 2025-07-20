import streamlit as st
from docx import Document
import os

def save_to_doc(text):
    try:
        file_path = ''
        doc = Document()
        doc.add_paragraph(text)
        doc.save(file_path)
        st.success(f'文件已保存到: {file_path}')
        print(f'文件已保存到: {file_path}')
    except Exception as e:
        st.error(f"出现错误：{e}")
