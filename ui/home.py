# app.py
import streamlit as st

from utils.file import remove_tmp_folder

st.set_page_config(
    page_title="首頁",
    page_icon="👋",
)
st.sidebar.header("首頁")
st.title("DOMjudge 題目管理工具")


content = """
目前處在開發階段，尚未提供任意功能。\n
當前支援的功能有：\n
- 暫無功能\n
待開發支援的功能有：\n
- 創建帳號功能 (emails)\n
- 考區設定功能 (general)\n
- 題目管理功能 (problems)\n
- 成績版功能 (scoreboard)\n
- 呈件功能 (submissions)\n
"""

st.write(content)

def clear_state():
    remove_tmp_folder()
    st.session_state.clear()

st.sidebar.button("清除暫存帳密", on_click=clear_state)
st.sidebar.button("取得 Judge 資訊")


host = st.text_input(
    "網址連結",
    key="host",
    value=None,
    placeholder="請輸入網址連結",
)

username = st.text_input(
    "帳號名稱",
    key="username",
    value=None,
    placeholder="請輸入帳號名稱",
)

password = st.text_input(
    "密碼",
    key="password",
    value=None,
    placeholder="請輸入密碼",
)

version = st.text_input(
    "Judge 版本",
    key="version",
    value="7.3.4",
    placeholder="請輸入 Judge 版本",
)

api_version = st.text_input(
    "API 版本",
    key="api_version",
    value="v4",
    placeholder="請輸入 API 版本",
)

st.button("登入")
st.button("註冊")
# st.button("新增範例測資", on_click=lambda: create_folder("data/sample"))


if __name__ == "__main__":
    import sys
    if "../" not in sys.path:
        sys.path.append("../")