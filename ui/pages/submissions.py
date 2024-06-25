import asyncio
import streamlit as st

from customization._submissions import get_submissions
from customization.submissions import submission_file, get_content_options, contest_files

from domjudge_tool_cli.commands.general import general_state, get_or_ask_config

from utils.check import login_required


@login_required
def get_submissions_record(contest_name):
    """
    Get submission record.
    """
    cid = st.session_state["content_option"][contest_name].CID
    client = get_or_ask_config(general_state["config"])
    st.session_state["subissions_record"] = asyncio.run(get_submissions(client, cid))


def check_mode_value(selected_mode):
    if selected_mode == "選擇一：team_name/problem_name/submission_file":
        return 1
    
    if selected_mode == "選擇二：problem_name/team_name/submission_file":
        return 2
    
    if selected_mode == "選擇三：contest_id/submission_file":
        return 3


@login_required
def submissions_page():
    st.set_page_config(page_title="管理提交紀錄頁面", page_icon="📄")
    st.sidebar.header("管理提交紀錄")
    st.title("管理提交紀錄")

    st.markdown('### 匯出單一提交紀錄')
    submission_file_form_cid_option = st.selectbox(
        "請選擇考區",
        options=st.session_state["content_option"],
        key="submission_file_form_cid_option",
    )

    if submission_file_form_cid_option:
        contest_name = submission_file_form_cid_option
        get_submissions_record(contest_name)

    submission_file_form_ids_options = st.multiselect(
    "選擇提交紀錄",
    st.session_state["subissions_record"],)

    submission_file_form_mode = st.selectbox(
        "輸出路徑樣式選擇",
        options=[
            "選擇一：team_name/problem_name/submission_file",
            "選擇二：problem_name/team_name/submission_file",
            "選擇三：contest_id/submission_file",
        ],
        key="submission_file_form_mode",
    )

    zip_filename = st.text_input(
        "ZIP 檔案名稱",
        key="submission_file_form_zip_filename",
        value=None,
        placeholder="請輸入 ZIP 檔案名稱",
    )

    col1, col2, col3, col4 = st.columns([2, 3, 3, 4])
    submission_file_submit = col1.button("匯出檔案")

    if submission_file_submit:
        try:
            ids = [st.session_state["subissions_record"][i].id for i in submission_file_form_ids_options]
            mode = check_mode_value(submission_file_form_mode)

            file_data = submission_file(
                cid=st.session_state["content_option"][submission_file_form_cid_option].CID,
                submission_ids=ids,
                mode=mode,
            )

            if file_data:
                col2.download_button(
                    label="下載提交紀錄",
                    data=file_data,
                    file_name=f"{zip_filename if zip_filename else 'export_forder'}.zip",
                    mime="application/zip",
                )

        except Exception as e:
            st.error(f"下載提交檔案失敗：{cid}，{e}")
    
    st.markdown('### 匯出提交紀錄')

    contest_files_form_cid_option = st.selectbox(
        "請選擇考區",
        options=st.session_state["content_option"],
        key="contest_files_form_cid_option",
    )

    contest_files_form_mode = st.selectbox(
        "輸出路徑樣式選擇",
        options=[
            "選擇一：team_name/problem_name/submission_file",
            "選擇二：problem_name/team_name/submission_file",
            "選擇三：contest_id/submission_file",
        ],
        key="contest_files_form_mode",
    )

    zip_filename = st.text_input(
        "ZIP 檔案名稱",
        key="contest_files_form_zip_filename",
        value=None,
        placeholder="請輸入 ZIP 檔案名稱",
    )

    col1, col2, col3, col4 = st.columns([3, 3, 4, 4])
    contest_files_submit = col1.button("匯出提交紀錄")

    if contest_files_submit:
        try:
            cid = st.session_state["content_option"][contest_files_form_cid_option].CID
            mode = check_mode_value(contest_files_form_mode)
            file_data = contest_files(
                cid=cid,
                mode=mode,
            )

            if file_data:
                col2.download_button(
                    label="下載壓縮檔",
                    data=file_data,
                    file_name=f'{zip_filename if zip_filename else "export_forder"}.zip',
                    mime="application/zip",
                )
            else:
                st.error("輸入的題目 ID 有誤")

            st.success(f"匯出提交紀錄成功")

        except Exception as e:
            st.error(f"匯出提交紀錄失敗：{e}")

if __name__ == "__main__":
    st.session_state["content_option"] = get_content_options()
    submissions_page()