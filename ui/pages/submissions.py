import streamlit as st

from domjudge_tool_cli.commands import submissions

st.set_page_config(page_title="顯示提交紀錄頁面", page_icon="📄")
st.sidebar.header("顯示提交紀錄")
st.title("顯示提交紀錄")

option = st.selectbox(
    "考場提交紀錄",
    ("Email", "Home phone", "Mobile phone"))

st.write("You selected:", option)

st.json({
    'foo': 'bar',
    'baz': 'boz',
    'stuff': [
        'stuff 1',
        'stuff 2',
        'stuff 3',
        'stuff 5',
    ],
})

st.button("下載考場提交紀錄")
st.button("下載全部考場提交紀錄")