import streamlit as st

from domjudge_tool_cli.commands.submissions import submission_list, submission_file, contest_files

from utils.check import login_required

@login_required
def submissions_page():
    st.set_page_config(page_title="管理提交紀錄頁面", page_icon="📄")
    st.sidebar.header("管理提交紀錄")
    st.title("管理提交紀錄")

    st.markdown('### 列出單一提交紀錄')
    submission_list_form = st.form("submission_list_form")

    cid = submission_list_form.text_input(
        "Contest ID",
        key="submission_list_form_cid",
        value=None,
        placeholder="請輸入 Contest ID",
    )

    language_id = submission_list_form.text_input(
        "Language ID",
        key="submission_list_form_language_id",
        value=None,
        placeholder="請輸入 Language ID",
    )

    strict = submission_list_form.checkbox(
        "Strict",
        key="submission_list_form_strict",
        value=False,
    )

    ids = submission_list_form.text_input(
        "Submission IDs",
        key="submission_list_form_ids",
        value=None,
        placeholder="請輸入 Submission IDs",
    )

    submission_list_submit = submission_list_form.form_submit_button("列出提交紀錄")

    if submission_list_submit:
        try:
            submission_list(
                cid=cid,
                language_id=language_id,
                strict=strict,
                ids=ids,
            )
            st.success(f"列出提交紀錄成功：{cid}")

        except Exception as e:
            st.error(f"列出提交紀錄失敗：{cid}，{e}")
    
    st.markdown('### 匯出單一提交紀錄')
    submission_file_form = st.form("submission_file_form")

    cid = submission_file_form.text_input(
        "Contest ID",
        key="submission_file_form_cid",
        value=None,
        placeholder="請輸入 Contest ID",
    )

    id = submission_file_form.text_input(
        "Submission ID",
        key="submission_file_form_id",
        value=None,
        placeholder="請輸入 Submission ID",
    )

    mode = submission_file_form.number_input(
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

    path = submission_file_form.text_input(
        "Path",
        key="submission_file_form_path",
        value=None,
        placeholder="請輸入 Path",
    )

    strict = submission_file_form.checkbox(
        "Strict",
        key="submission_file_form_strict",
        value=False,
    )

    is_extract = submission_file_form.checkbox(
        "Is Extract",
        key="submission_file_form_is_extract",
        value=True,
    )

    st.markdown('### 匯出提交紀錄')
    submission_file_submit = submission_file_form.form_submit_button("下載提交檔案")

    if submission_file_submit:
        try:
            submission_file(
                cid=cid,
                id=id,
                mode=mode,
                path=path,
                strict=strict,
                is_extract=is_extract,
            )
            st.success(f"下載提交檔案成功：{cid}")

        except Exception as e:
            st.error(f"下載提交檔案失敗：{cid}，{e}")
    
    contest_files_form = st.form("contest_files_form")

    cid = contest_files_form.text_input(
        "Contest ID",
        key="contest_files_form_cid",
        value=None,
        placeholder="請輸入 Contest ID",
    )

    mode = contest_files_form.number_input(
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

    path = contest_files_form.text_input(
        "Path",
        key="contest_files_form_path",
        value=None,
        placeholder="請輸入 Path",
    )

    strict = contest_files_form.checkbox(
        "Strict",
        key="contest_files_form_strict",
        value=False,
    )

    is_extract = contest_files_form.checkbox(
        "Is Extract",
        key="contest_files_form_is_extract",
        value=True,
    )

    contest_files_submit = contest_files_form.form_submit_button("下載提交檔案")

    if contest_files_submit:
        try:
            contest_files(
                cid=cid,
                mode=mode,
                path=path,
                strict=strict,
                is_extract=is_extract,
            )
            st.success(f"下載提交檔案成功")

        except Exception as e:
            st.error(f"下載提交檔案失敗：{e}")

if __name__ == "__main__":
    submissions_page()