# app.py
import json
import os

import streamlit as st
from domjudge_tool_cli.commands import general

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

if os.path.exists("domserver.json"):
    with open("domserver.json", "r") as f:
        domserver = json.load(f)
else:
    domserver = dict()

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
st.sidebar.button("清除暫存帳密", on_click=clear_owner)
# st.sidebar.button("取得 Judge 資訊")

animal = st.form("my_animal")

host = animal.text_input(
    "網址連結",
    key="host",
    value=domserver.get("host", "https://127.0.0.1:8000/"),
    placeholder="請輸入網址連結",
)

username = animal.text_input(
    "帳號名稱",
    key="username",
    value=domserver.get("username", "admin"),
    placeholder="請輸入帳號名稱",
)

password = animal.text_input(
    "密碼",
    key="password",
    value=domserver.get("password", None),
    placeholder="請輸入密碼",
    type="password",
)

version = animal.text_input(
    "Judge 版本",
    key="version",
    value=domserver.get("version", "7.3.4"),
    placeholder="請輸入 Judge 版本",
)

api_version = animal.text_input(
    "API 版本",
    key="api_version",
    value=domserver.get("api_version", "v4"),
    placeholder="請輸入 API 版本",
)

disable_ssl = animal.checkbox(
    "Disable SSL",
    key="disable_ssl",
    value=domserver.get("disable_ssl", False),
)
timeout = animal.number_input(
    "Timeout",
      key="timeout", 
      value=domserver.get("timout", 1.00), format="%.2f",
      placeholder="請輸入 Timeout 時間",
)
max_connections = animal.number_input(
    "Max Connections", 
    key="max_connections", 
    value=domserver.get("max_connections", 10),
    placeholder="請輸入 Max Connections 數量",
)
max_keepalive_connections = animal.number_input(
    "Max Keepalive Connections",
    key="max_keepalive_connections",
    value=domserver.get("max_keepalive_connections", 10),
    placeholder="請輸入 Max Keepalive Connections 數量",
)

submit = animal.form_submit_button("登入")

if submit:
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

    try:
        test = general.check(
            host=host,
            username=username,
            password=password,
        )
        st.success(f"登入成功")
        st.session_state["logged_in"] = True

    except Exception as e:
        st.error(f"錯誤：{e}")
        st.session_state["logged_in"] = False