# app.py
import streamlit as st

from customization import general

st.set_page_config(
    page_title="首頁",
    page_icon="👋",
)

def clear_owner():
    if st.session_state.get("user_info"):
        st.session_state["user_info"] = None
        st.success("清除成功")


def home_page():
    st.sidebar.header("首頁")
    st.title("DOMjudge 題目管理工具")

    content = """
    當前支援的功能有：\n
    - 寄送帳號功能 (emails)\n
    - 題目匯出功能 (problems)\n
    - 成績版功能 (scoreboard)\n
    - 提交紀錄匯出功能 (submissions)\n
    - 查看紀錄功能 (viewsubmission)\n
    - 帳號查詢功能 (users info)\n
    - 帳號匯入功能 (users)\n
    """

    st.write(content)
    st.sidebar.button("清除暫存帳密", on_click=clear_owner)

    domserver = dict()
    if st.session_state.get("user_info"):
        domserver = st.session_state["user_info"]

    login_form = st.form("login_form")

    host = login_form.text_input(
        "網址連結",
        key="host",
        value=domserver.get("host", "http://127.0.0.1:8000/"),
        placeholder="請輸入網址連結",
    )

    username = login_form.text_input(
        "帳號名稱",
        key="username",
        value=domserver.get("username", "admin"),
        placeholder="請輸入帳號名稱",
    )

    password = login_form.text_input(
        "密碼",
        key="password",
        value=domserver.get("password", None),
        placeholder="請輸入密碼",
        type="password",
    )

    version = login_form.text_input(
        "Judge 版本",
        key="version",
        value=domserver.get("version", "7.3.4"),
        placeholder="請輸入 Judge 版本",
    )

    api_version = login_form.text_input(
        "API 版本",
        key="api_version",
        value=domserver.get("api_version", "v4"),
        placeholder="請輸入 API 版本",
    )

    disable_ssl = login_form.checkbox(
        "Disable SSL",
        key="disable_ssl",
        value=domserver.get("disable_ssl", False),
    )
    timeout = login_form.number_input(
        "Timeout",
        key="timeout", 
        value=domserver.get("timeout", 1.0), format="%.2f",
        placeholder="請輸入 Timeout 時間",
    )
    max_connections = login_form.number_input(
        "Max Connections", 
        key="max_connections", 
        value=domserver.get("max_connections", 10),
        placeholder="請輸入 Max Connections 數量",
    )
    max_keepalive_connections = login_form.number_input(
        "Max Keepalive Connections",
        key="max_keepalive_connections",
        value=domserver.get("max_keepalive_connections", 10),
        placeholder="請輸入 Max Keepalive Connections 數量",
    )

    submit = login_form.form_submit_button("設定與登入")

    if submit:
        
        try:
            parms = {
                "version": version,
                "api_version": api_version,
                "disable_ssl": disable_ssl,
                "timeout": timeout,
                "max_connections": max_connections,
                "max_keepalive_connections": max_keepalive_connections,
            }

            client = general.check(
                host=host,
                username=username,
                password=password,
                **parms,
            )

            if client:
                st.success(f"登入成功")
                st.session_state["user_info"] = {
                    **client.dict(),
                }
            
            else:
                st.error(f"登入失敗")

        except Exception as e:
            st.error(f"登入失敗, {e}")


if __name__ == "__main__":
    home_page()