import asyncio
import streamlit as st

# from domjudge_tool_cli.commands.submissions import submission_list, submission_file, contest_files
from customization.submissions import submission_list, submission_file, get_content_options, contest_files
from domjudge_tool_cli.commands.general import general_state, get_or_ask_config
from customization._submissions import get_submissions, judgement_submission_mapping

from utils.check import login_required


@login_required
def get_submissions_record(contest_name):
    """
    Get submission record.
    """
    cid = st.session_state["content_option"][contest_name].CID
    client = get_or_ask_config(general_state["config"])
    st.session_state["subissions_record"] = asyncio.run(get_submissions(client, cid))


# @login_required
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

    submission_file_form_mode = st.number_input(
        "Mode",
        key="submission_file_form_mode",
        value=2,
        placeholder="請輸入 Mode",
        help="""
            Output path format mode:\n
            mode=1: team_name/problem_name/submission_file.
            mode=2: problem_name/team_name/submission_file.
            other: contest_id/submission_file
            """,
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
            
            file_data = submission_file(
                cid=st.session_state["content_option"][submission_file_form_cid_option].CID,
                submission_ids=ids,
                mode=submission_file_form_mode,
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

    contest_files_form_mode = st.number_input(
        "Mode",
        key="contest_files_form_mode",
        value=2,
        placeholder="請輸入 Mode",
        help="""
            Output path format mode:\n
            mode=1: team_name/problem_name/submission_file.
            mode=2: problem_name/team_name/submission_file.
            other: contest_id/submission_file
            """,
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
            file_data = contest_files(
                cid=cid,
                mode=contest_files_form_mode,
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