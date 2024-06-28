import os
import streamlit as st

from customization.users import (
    get_affiliations_options,
    get_categories_options,
)
from customization.users import import_users_teams

from utils.check import login_required
from utils.users import UserRoles


st.set_page_config(page_title="創建帳號頁面", page_icon="📄")

@st.cache_data
def convert_df(pkg_path):
    path = os.path.join(os.path.dirname(__file__), pkg_path)

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    return content

@login_required
def users_page():
    category_options = get_categories_options()
    affiliation_dict = {affiliation.shortname: affiliation.id for affiliation in get_affiliations_options()}

    st.sidebar.header("創建帳號")
    st.title("創建帳號")

    csv = convert_df("../templates/csv/import-users-teams.csv")
    st.download_button(
        label="Download Example Data as CSV",
        data=csv,
        file_name="example_users_teams.csv",
        mime="text/csv",
    )

    user_csv = st.file_uploader("開啟帳號 .csv 檔案", type="csv")

    if category_options:
        category = st.selectbox(
            "類別",
            options=category_options,
            key="category",
        )

    if affiliation_dict:
        affiliation_select = st.selectbox(
            "隸屬",
            options=affiliation_dict.keys(),
            key="affiliation_select",
        )

    user_roles = st.multiselect(
    "user_roles",
    UserRoles.__members__.keys(),
    )

    enabled = st.checkbox(
        "Enabled",
        key="enabled",
        value=True,
    )

    ignore_existing = st.checkbox(
        "Ignore Existing",
        key="ignore_existing",
        value=False,
    )

    delete_existing = st.checkbox(
        "Delete Existing",
        key="delete_existing",
        value=False,
    )

    password_length = st.text_input(
        "Password Length",
        key="password_length",
        value=None,
        placeholder="請輸入 Password Length",
    )

    password_pattern = st.text_input(
        "Password Pattern",
        key="password_pattern",
        value=None,
        placeholder="Random charset, ex: 0123456789",
    )

    new_password = st.checkbox(
        "New Password",
        key="new_password",
        value=False,
    )

    col1, col2, col3, col4 = st.columns([2, 2, 4, 4])

    if col1.button("創建"):
        try:
            if not user_csv or not user_roles:
                st.warning("檢查 csv 檔案和用戶角色是否選擇")

            else:
                category_id = category_options.get(category).ID
                affiliation_id = affiliation_dict[affiliation_select]
                user_roles = [int(UserRoles.__members__[role].value) for role in user_roles]

                csv_data = import_users_teams(
                    file=user_csv,
                    category_id=category_id,
                    affiliation_id=affiliation_id,
                    user_roles=user_roles,
                    enabled=enabled,
                    ignore_existing=ignore_existing,
                    delete_existing=delete_existing,
                    password_length=int(password_length) if password_length else None,
                    password_pattern=password_pattern,
                    new_password=new_password,
                )    
                
                col2.download_button(
                    label="下載檔案",
                    data=csv_data,
                    file_name=f'user_teams.csv',
                    mime="text/csv",
                )

                st.success(f"創建成功")

        except Exception as e:
            st.error(f"錯誤：{e}")


if __name__ == "__main__":
    users_page()