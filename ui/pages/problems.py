import os
import asyncio
import pandas as pd
import streamlit as st

from domjudge_tool_cli.commands.general import get_or_ask_config
from domjudge_tool_cli.commands.problems import download_problems

from utils.check import login_required
from utils.web import get_session

st.set_page_config(page_title="題目管理頁面", page_icon="📄")

async def get_problems_info(client):
    web = await get_session(client=client)
    problems = await web.get_problems(exclude=list())
    
    return problems if problems is not None else list()

@login_required
def problems_page():
    client = get_or_ask_config()
    problems = asyncio.run(get_problems_info(client=client))

    st.sidebar.header("題目管理")
    st.title("題目管理")

    problems_dict = [problem.__dict__ for problem in problems]
    df = pd.DataFrame(problems_dict)
    df = df.drop(columns=["export_file_path"])

    st.table(df)

    exclude_id = st.text_input("需要排除的題目 ID", placeholder="ex: problemId1,problemId2")
    only_id = st.text_input("需要匯出的題目 ID", placeholder="ex: problemId1,problemId2")
    folder = st.text_input("需要匯出的資料夾名稱", placeholder="Export folder name")

    export_button = st.button("匯出題目")
    
    if export_button:
        try:
            download_problems(exclude_id, only_id, folder)
            st.write("資料夾路徑：", f"{os.path.abspath(folder)}")
            st.success("匯出成功")
        except Exception as e:
            st.error("匯出失敗：", e)


if __name__ == "__main__":
    problems_page()