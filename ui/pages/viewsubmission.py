import asyncio
import streamlit as st

# from domjudge_tool_cli.commands.submissions import submission_list, submission_file, contest_files
from customization.submissions import submission_list, submission_file, get_content_options, get_language_options, contest_files, view_submission
from domjudge_tool_cli.commands.general import general_state, get_or_ask_config
from customization._submissions import get_submissions, judgement_submission_mapping

from utils.check import login_required


@login_required
def get_submissions_record(contest_name, language_name=None):
    """
    Get submission record.
    """
    lid = language_name
    cid = st.session_state["content_options"][contest_name].CID
    if language_name:
        lid = st.session_state["language_options"][language_name].LID

    client = get_or_ask_config(general_state["config"])
    st.session_state["submissions"] = asyncio.run(get_submissions(client, cid, lid))


# @login_required
def submissions_page():
    st.set_page_config(page_title="管理提交紀錄頁面", page_icon="📄")
    st.sidebar.header("管理提交紀錄")
    st.title("管理提交紀錄")

    st.markdown('### 列出單一提交紀錄')

    contest_option = st.selectbox(
        "請選擇考區",
        options=st.session_state["content_options"],
        key="contest_option",
    )

    if contest_option:
        contest_name = contest_option
        get_submissions_record(contest_name)

    language_option = st.selectbox(
        "選擇語言",
        options=st.session_state["language_options"],

    )

    if language_option != "All":
        language_name = language_option
        get_submissions_record(contest_name, language_name)

    submission_id_option = st.selectbox(
        "選擇提交紀錄",
        st.session_state["submissions"],
    )

    submission_submit = st.button("列出提交紀錄")

    if submission_submit:
        try:
            cid = st.session_state["content_options"][contest_option].CID
            submission_id = st.session_state["submissions"][submission_id_option].id

            st.session_state["submission_source_code"] = view_submission(
                cid=cid,
                id=submission_id,
            )

        except Exception as e:
            st.error(f"列出提交紀錄失敗：{cid}，{e}")


    if st.session_state["submission_source_code"]:
        st.markdown('### 提交紀錄')
        code = f'''{st.session_state["submission_source_code"]}'''
        st.code(code, language='python')
    

if __name__ == "__main__":
    st.session_state["submission_source_code"] = None
    st.session_state["content_options"] = get_content_options()
    st.session_state["language_options"] = get_language_options()
    submissions_page()