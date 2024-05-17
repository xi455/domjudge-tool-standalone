import streamlit as st

from domjudge_tool_cli.commands import scoreboard

st.set_page_config(page_title="分數頁面", page_icon="📄")
st.sidebar.header("分數")
st.title("分數")

option = st.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone"))

st.write("You selected:", option)

file_name = st.text_input("壓縮檔名稱")