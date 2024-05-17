import streamlit as st
import pandas as pd
import numpy as np

from domjudge_tool_cli.commands import problems

st.set_page_config(page_title="題目管理頁面", page_icon="📄")
st.sidebar.header("題目管理")
st.title("題目管理")

df = pd.DataFrame(np.random.randn(10, 3), columns=("col %d" % i for i in range(3)))

st.table(df)

export_file_name = st.text_input("題目匯出壓縮檔名稱")
uploaded_problem_zip = st.file_uploader("上傳題目 .zip 檔案", type="zip")