import os
import time
from math import ceil
import pandas as pd
import streamlit as st
import mysql.connector

conn = mysql.connector.connect(

)
c = conn.cursor()

st.header("实时水质监控")

st.caption("历史数据：")

query_all = "SELECT * FROM water_quality"
df = pd.read_sql(query_all, conn)

query = "SELECT * FROM water_quality ORDER BY id DESC LIMIT 1"
c.execute(query)
last_record = c.fetchone()

if last_record:
    last_values = {
        'turbidity': last_record[1],
        'pH': last_record[2],
        'ammonia_nitrogen': last_record[3],
        'dissolved_oxygen': last_record[4]
    }
else:
    last_values = {'turbidity': 0, 'pH': 0, 'ammonia_nitrogen': 0, 'dissolved_oxygen': 0}

# 分页设置
page_size = 10
total_pages = ceil(len(df) / page_size)

if "curr_page" not in st.session_state.keys():
    st.session_state.curr_page = 1

curr_page = min(st.session_state['curr_page'], total_pages)

# 显示分页按钮
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

docs = st.dataframe(
    df_paginated,
    width=1050,
    column_config={
        "id": None,  # 隐藏
        "turbidity": "透明度",
        "pH": "pH值",
        "ammonia_nitrogen": "氨氮含量",
        "dissolved_oxygen": "溶解氧",
    },
    hide_index=True,
    on_select="rerun",
    selection_mode="multi-row",
)

selected_docs = docs.selection.rows
if len(selected_docs) > 0:
    delete_button = st.button("删除选中的数据", key="delete_docs")
    if delete_button:
        print("Deleting records...")
        with st.spinner(text="正在删除数据。"):
            for item in selected_docs:
                record_id = df_paginated.iloc[item]['id']
                c.execute("DELETE FROM water_quality WHERE id = %s", (record_id,))
            conn.commit()
            time.sleep(3)
            st.toast('✔️ 选择的数据已删除！', icon='🎉')
            st.rerun()

# 数字输入框和监控组件
col1, col2 = st.columns(2)
with col1:
    turbidity = st.number_input("透明度", value=last_values['turbidity'])
    st.metric("透明度", turbidity, delta=turbidity - last_values['turbidity'])
    ammonia_nitrogen = st.number_input("氨氮含量", value=last_values['ammonia_nitrogen'])
    st.metric("氨氮含量", ammonia_nitrogen, delta=ammonia_nitrogen - last_values['ammonia_nitrogen'])

with col2:
    pH = st.number_input("pH值", value=last_values['pH'])
    st.metric("pH值", pH, delta=pH - last_values['pH'])
    dissolved_oxygen = st.number_input("溶解氧", value=last_values['dissolved_oxygen'])
    st.metric("溶解氧", dissolved_oxygen, delta=dissolved_oxygen - last_values['dissolved_oxygen'])

if st.button("提交到数据库"):
    c.execute('''
    INSERT INTO water_quality (turbidity, pH, ammonia_nitrogen, dissolved_oxygen)
    VALUES (%s, %s, %s, %s)
    ''', (turbidity, pH, ammonia_nitrogen, dissolved_oxygen))
    conn.commit()
    time.sleep(3)
    st.success("数据已保存到数据库.")
    st.rerun()

conn.close()
