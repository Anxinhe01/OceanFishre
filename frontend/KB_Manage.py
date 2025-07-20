import os
import time
from math import ceil
import pandas as pd
import streamlit as st


def get_unique_files_info(ref_doc_info):
    docs = []
    seen_paths = set()

    for ref_doc_id, ref_doc in ref_doc_info.items():

        metadata = ref_doc.metadata
        file_path = metadata.get('file_path', None)

        if file_path is None:
            title = metadata.get('title', None)
            url = metadata.get('url_source', None)
            docs.append({
                'id': ref_doc_id,
                'name': title,
                'type': "url",
                'path': url,
                'date': metadata['creation_date']
            })

        if file_path and file_path not in seen_paths:
            base_name, extension = os.path.splitext(metadata['file_name'])
            # Remove the leading dot from the extension
            extension = extension.lstrip('.')

            file_info = {
                'id': ref_doc_id,
                'name': base_name,
                'type': extension,
                'path': file_path,
                # 'file_size': metadata['file_size'],
                'date': metadata['creation_date']
            }
            docs.append(file_info)
            seen_paths.add(file_path)

    return docs


def handle_knowledgebase():
    st.header("进行文件管理")
    st.caption("管理知识库中的文档。（在前面进行选择。部分新加载的文档可能需要重启才能生效。）")

    from server.stores.strage_context import STORAGE_CONTEXT
    doc_store = STORAGE_CONTEXT.docstore
    if len(doc_store.docs) > 0:
        ref_doc_info = doc_store.get_all_ref_doc_info()
        unique_files = get_unique_files_info(ref_doc_info)
        st.write("一共有：", len(unique_files), "个文件.")
        df = pd.DataFrame(unique_files)

        # Pagination settings

        page_size = 10
        total_pages = ceil(len(df) / page_size)

        if "curr_page" not in st.session_state.keys():
            st.session_state.curr_page = 1

        curr_page = min(st.session_state['curr_page'], total_pages)

        # Displaying pagination buttons
        if total_pages > 1:
            prev, next, _, col3 = st.columns([1, 1, 6, 2])

            if next.button("下一页"):
                curr_page = min(curr_page + 1, total_pages)
                st.session_state['curr_page'] = curr_page

            if prev.button("上一页"):
                curr_page = max(curr_page - 1, 1)
                st.session_state['curr_page'] = curr_page

            with col3:
                st.write("当前页/总页数: ", curr_page, "/", total_pages)

        start_index = (curr_page - 1) * page_size
        end_index = curr_page * page_size
        df_paginated = df.iloc[start_index:end_index]

        # Displaying the paginated dataframe
        docs = st.dataframe(
            df_paginated,
            width=2000,
            column_config={
                "id": None,  # hidden
                "name": "名称",
                "type": "格式",
                "path": None,
                "date": "上传日期",

            },
            hide_index=True,
            on_select="rerun",
            selection_mode="multi-row",
        )

        selected_docs = docs.selection.rows
        if len(selected_docs) > 0:
            delete_button = st.button("删除选中的文件", key="delete_docs")
            if delete_button:
                print("Deleting documents...")
                with st.spinner(text="正在删除文档和相关索引。这可能需要几分钟的时间。"):
                    for item in selected_docs:
                        path = df_paginated.iloc[item]['path']
                        for ref_doc_id, ref_doc in ref_doc_info.items():  # a file may have multiple documents
                            metadata = ref_doc.metadata
                            file_path = metadata.get('file_path', None)
                            if file_path:
                                if file_path == path:
                                    st.session_state.index_manager.delete_ref_doc(ref_doc_id)
                            elif metadata.get('url_source', None) == path:
                                st.session_state.index_manager.delete_ref_doc(ref_doc_id)
                    st.toast('✔️ 选择的文档已删除！', icon='🎉')
                    time.sleep(4)
                    st.rerun()

            st.write("选中的文件:")
            for item in selected_docs:
                st.write(f"- {df_paginated.iloc[item]['name']}")

    else:
        st.write("知识库为空！前往‘文件上传’页面上传文件！")


handle_knowledgebase()


