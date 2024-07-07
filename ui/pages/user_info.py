import pandas as pd
import streamlit as st

from utils.check import login_required

from customization.users import (
    user_list,
    create_category,
)


st.set_page_config(page_title="用戶資訊頁面", page_icon="📄")

@login_required
def handle_table_pagination(users_dict):
    df = pd.DataFrame(users_dict)
    st.write(df)


@login_required
def user_info_page():
    users_dict = [user.__dict__ for user in user_list()]

    st.sidebar.header("用戶資訊")
    st.title("用戶資訊")

    # # 顯示資料
    handle_table_pagination(users_dict)

    st.title("建立類別")

    category = st.text_input(
        "新建類別",
        key="new_category",
        value=None,
        placeholder="請輸入新類別名稱",
    )

    sortorder = st.text_input(
        "排序",
        key="sortorder",
        value=None,
        placeholder="請輸入排序數字",
    )

    color = st.text_input(
        "顏色",
        key="color",
        value=None,
        placeholder="請輸入顏色 ex: #000000",
    )

    visible = st.checkbox(
        "可見",
        key="visible",
        value=True,
    )

    allow_self_registration = st.checkbox(
        "允許自我註冊",
        key="allow_self_registration",
        value=False,
    )

    if st.button("建立"):
        try:
            create_category(
                name=category,
                sortorder=sortorder if sortorder else None,
                color=color,
                visible=visible,
                allow_self_registration=allow_self_registration,
            )
            st.success(f"已建立新類別: {category}")
        except Exception as e:
            st.error(f"建立新類別失敗: {e}")

if __name__ == "__main__":
    user_info_page()