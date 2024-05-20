import os
import streamlit as st

from domjudge_tool_cli.commands.scoreboard import export
from domjudge_tool_cli.commands.general import get_or_ask_config

from utils.check import login_required

@login_required
def scoreboard_page():
    st.set_page_config(page_title="匯出分數頁面", page_icon="📄")
    st.sidebar.header("匯出分數")
    st.title("匯出分數")

    domserver = None
    if os.path.exists("domserver.json"):
        domserver = get_or_ask_config()
        
    cid = st.number_input(
        "Contest ID",
        key="cid",
        value=None,
        placeholder="請輸入 cid",
    )

    filename = st.text_input(
        "檔案名稱",
        key="filename",
        value= "export",
        placeholder="請輸入檔案名稱",
    )

    url = st.text_input(
        "網址連結",
        key="url",
        value= domserver.host if domserver and domserver.host else "http://127.0.0.1:8000/",
        placeholder="請輸入網址連結",
    )

    path_prefix = st.text_input(
        "路徑前綴",
        key="path_prefix",
        value=None,
        placeholder="請輸入路徑前綴",
    )

    export_button = st.button("匯出分數")
    if export_button:
        try:
            export(cid, filename, url, path_prefix)
            st.success("匯出成功")
        except Exception as e:
            st.error("匯出失敗：", e)

if __name__ == "__main__":
    scoreboard_page()