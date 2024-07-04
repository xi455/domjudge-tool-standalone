import streamlit as st
from pydantic import ValidationError

from customization.submissions import get_content_options, get_language_options, view_submission

from utils.check import login_required
from utils.submissions import get_submissions_record


@login_required
def submissions_page():
    content_option_dict = get_content_options()
    language_option_dict = get_language_options()

    st.set_page_config(page_title="管理提交紀錄頁面", page_icon="📄")
    st.sidebar.header("管理提交紀錄")
    st.title("管理提交紀錄")

    st.markdown('### 列出單一提交紀錄')

    contest_option = st.selectbox(
        "請選擇考區",
        options=content_option_dict,
        key="contest_option",
    )

    if contest_option:
        contest_name = contest_option

        try:
            subissions_record_dict = get_submissions_record(content_option_dict, contest_name)

        except ValidationError as e:
            st.error(f"無法取得提交紀錄，請檢查 網址連結 SSL 是否設定正確")

    language_option = st.selectbox(
        "選擇語言",
        options=language_option_dict,

    )

    if language_option != "All":
        language_name = language_option

        try:
            subissions_record_dict = get_submissions_record(content_option_dict, contest_name, language_option_dict, language_name)

        except ValidationError as e:
            st.error(f"無法取得提交紀錄，請檢查 url SSL 是否設定正確")

    if "subissions_record_dict" in locals():
        submission_id_option = st.selectbox(
            "選擇提交紀錄",
            subissions_record_dict,
        )

        submission_submit = st.button("列出提交紀錄")
    
    else:
        submission_submit = st.button("列出提交紀錄", disabled=True)

    if submission_submit:
        try:
            cid = content_option_dict[contest_option].cid
            submission_id = subissions_record_dict[submission_id_option].id

            st.session_state["submission_source_code"] = view_submission(
                cid=cid,
                id=submission_id,
            )

        except Exception as e:
            st.error(f"列出提交紀錄失敗：{e}")


    if st.session_state["submission_source_code"]:
        st.markdown('### 提交紀錄')
        code = f'''{st.session_state["submission_source_code"]}'''
        st.code(code, language='python')
    

if __name__ == "__main__":
    st.session_state["submission_source_code"] = None

    submissions_page()