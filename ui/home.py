# app.py
import os

from pydantic import ValidationError
import streamlit as st
from domjudge_tool_cli.commands.general import get_or_ask_config

st.set_page_config(
    page_title="首頁",
    page_icon="👋",
)

def clear_owner():
    if os.path.exists("domserver.json"):
        os.remove("domserver.json")
        st.success("清除成功")

st.sidebar.header("首頁")
st.title("DOMjudge 題目管理工具")

content = """
當前支援的功能有：\n
- 寄送帳號功能 (emails)\n
- 題目匯出功能 (problems)\n
- 成績版功能 (scoreboard)\n
- 提交紀錄匯出功能 (submissions)\n
- 查看紀錄功能 (viewsubmission)\n
"""

st.write(content)
st.sidebar.button("清除暫存帳密", on_click=clear_owner)

domserver = None
if os.path.exists("domserver.json"):
    domserver = get_or_ask_config()

login_form = st.form("login_form")

host = login_form.text_input(
    "網址連結",
    key="host",
    value=domserver.host if domserver and domserver.host else "http://127.0.0.1:8000/",
    placeholder="請輸入網址連結",
)

username = login_form.text_input(
    "帳號名稱",
    key="username",
    value=domserver.username if domserver and domserver.username else "admin",
    placeholder="請輸入帳號名稱",
)

password = login_form.text_input(
    "密碼",
    key="password",
    value=domserver.password if domserver and domserver.password else None,
    placeholder="請輸入密碼",
    type="password",
)

version = login_form.text_input(
    "Judge 版本",
    key="version",
    value=domserver.version if domserver and domserver.version else "7.3.4",
    placeholder="請輸入 Judge 版本",
)

api_version = login_form.text_input(
    "API 版本",
    key="api_version",
    value=domserver.api_version if domserver and domserver.api_version else "v4",
    placeholder="請輸入 API 版本",
)

disable_ssl = login_form.checkbox(
    "Disable SSL",
    key="disable_ssl",
    value=domserver.disable_ssl if domserver and domserver.disable_ssl else False,
)
timeout = login_form.number_input(
    "Timeout",
      key="timeout", 
      value=domserver.timeout if domserver and domserver.timeout else 1.0, format="%.2f",
      placeholder="請輸入 Timeout 時間",
)
max_connections = login_form.number_input(
    "Max Connections", 
    key="max_connections", 
    value=domserver.max_connections if domserver and domserver.max_connections else 10,
    placeholder="請輸入 Max Connections 數量",
)
max_keepalive_connections = login_form.number_input(
    "Max Keepalive Connections",
    key="max_keepalive_connections",
    value=domserver.max_keepalive_connections if domserver and domserver.max_keepalive_connections else 10,
    placeholder="請輸入 Max Keepalive Connections 數量",
)

submit = login_form.form_submit_button("設定與登入")

from customization import general
if submit:
    try:
        owner_info = general.config(
            host=host,
            username=username,
            password=password,
            version=version,
            api_version=api_version,
            disable_ssl=disable_ssl,
            timeout=timeout,
            max_connections=max_connections,
            max_keepalive_connections=max_keepalive_connections,
        )

    except ValidationError as e:
        st.error(f"錯誤：{e}")

    try:
        general.check(
            host=host,
            username=username,
            password=password,
        )
        st.success(f"登入成功")
        st.session_state["logged_in"] = True

    except Exception as e:
        st.error(f"登入失敗")
        st.session_state["logged_in"] = False