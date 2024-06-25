import streamlit as st

from functools import wraps


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "logged_in" in st.session_state and st.session_state["logged_in"]:
            # 如果使用者已經登入，則執行原始函數
            return func(*args, **kwargs)
        else:
            # 如果使用者還沒有登入，則顯示一個錯誤訊息
            st.error("請先登入")

    return wrapper