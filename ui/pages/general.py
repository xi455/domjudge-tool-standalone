import streamlit as st
import pandas as pd
import numpy as np

from domjudge_tool_cli.commands import general

st.set_page_config(page_title="考區設定", page_icon="📄")
st.sidebar.header("考區設定")

st.title("考區設定")

df = pd.DataFrame(np.random.randn(10, 3), columns=("col %d" % i for i in range(3)))

st.table(df)

category_id = st.number_input(
    "類別",
    key="category_id",
    value=None,
    placeholder="請輸入類別",
)

affiliation_id = st.number_input(
    "隶屬關係",
    key="affiliation_id",
    value=None,
    placeholder="請輸入隶屬關係",
)

user_roles = st.number_input(
    "使用團隊",
    key="user_roles",
    value=None,
    placeholder="ex: role_id,role_id2,role_id3",
)