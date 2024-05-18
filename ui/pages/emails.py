import streamlit as st

from domjudge_tool_cli.commands import emails

from utils.login import login_required

st.set_page_config(page_title="創建帳號頁面", page_icon="📄")


@login_required
def emails_page():
    st.sidebar.header("創建帳號")
    st.title("創建帳號")

    uploaded_problem_zip = st.file_uploader("開啟帳號 .csv 檔案", type="csv")


if __name__ == "__main__":
    emails_page()
