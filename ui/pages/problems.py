import os
import asyncio
import pandas as pd
import streamlit as st

from domjudge_tool_cli.commands.general import get_or_ask_config
from customization.problems import download_problems

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

    items_per_page = 10

    # 讓使用者輸入頁碼
    page_number = st.number_input(label="頁碼", min_value=1, value=1, step=1)

    # 計算 start 和 end
    start = (page_number - 1) * items_per_page
    end = start + items_per_page

    # 顯示資料
    st.table(df.iloc[start:end])

    exclude_id = st.text_input("需要排除的題目 ID", placeholder="ex: problemId1,problemId2")
    only_id = st.text_input("需要匯出的題目 ID", placeholder="ex: problemId1,problemId2")
    folder = st.text_input("需要匯出的資料夾名稱", placeholder="Export folder name")

    col1, col2, col3, col4 = st.columns([2, 2, 4, 4])
    check_button = col1.button("確認題目")
    
    if check_button:
        try:
            file_name, file_data = download_problems(exclude_id, only_id, folder)
            
            if file_data:
                col2.download_button(
                    label="下載問題",
                    data=file_data,
                    file_name=f'{file_name if file_name else "export_forder"}.zip',
                    mime="application/zip",
                )
            else:
                st.error("輸入的題目 ID 有誤")
                
        except Exception as e:
            st.error(f"匯出失敗： {e}")


if __name__ == "__main__":
    problems_page()