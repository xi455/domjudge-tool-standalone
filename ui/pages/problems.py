import pandas as pd
import streamlit as st

from customization.problems import download_problems, get_problems_info

from utils.check import login_required



st.set_page_config(page_title="題目管理頁面", page_icon="📄")

@login_required
def handle_table_pagination(problems_dict):
    st.dataframe(pd.DataFrame(problems_dict))


@login_required
def problems_page():
    problems_dict = [problem.__dict__ for problem in get_problems_info()]

    st.sidebar.header("題目管理")
    st.title("題目管理")

    handle_table_pagination(problems_dict)

    exclude_id = st.text_input("需要排除的題目 ID", placeholder="ex: problemId1,problemId2")
    only_id = st.text_input("需要匯出的題目 ID", placeholder="ex: problemId1,problemId2")
    folder = st.text_input("需要匯出的壓縮檔名稱", placeholder="Export folder name")

    col1, col2, col3, col4 = st.columns([2, 2, 4, 4])
    check_button = col1.button("匯出題目")
    
    if check_button:
        try:
            file_name, file_data = download_problems([exclude_id], [only_id], folder)
            
            if file_data:
                col2.download_button(
                    label="下載問題",
                    data=file_data,
                    file_name=f'{file_name if file_name else "export_forder"}.zip',
                    mime="application/zip",
                )
            else:
                st.error("輸入的題目 ID 有誤")

            st.success(f"匯出檔案成功")
                
        except Exception as e:
            st.error(f"匯出失敗： {e}")


if __name__ == "__main__":
    problems_page()