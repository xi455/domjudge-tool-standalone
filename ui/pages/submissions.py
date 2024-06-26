import streamlit as st

from customization.submissions import submission_file, get_content_options, contest_files

from utils.check import login_required
from utils.submissions import get_submissions_record, check_mode_value


@login_required
def submissions_page(content_option_dict):
    st.set_page_config(page_title="管理提交紀錄頁面", page_icon="📄")
    st.sidebar.header("管理提交紀錄")
    st.title("管理提交紀錄")

    st.markdown('### 匯出單一提交紀錄')
    submission_file_form_cid_option = st.selectbox(
        "請選擇考區",
        options=content_option_dict,
        key="submission_file_form_cid_option",
    )

    if submission_file_form_cid_option:
        contest_name = submission_file_form_cid_option
        subissions_record_dict = get_submissions_record(content_option_dict, contest_name)

    submission_file_form_ids_options = st.multiselect(
    "選擇提交紀錄",
    subissions_record_dict,)

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
    submission_file_submit = col1.button("匯出檔案", key="submission_file_submit")

    if submission_file_submit:
        try:
            ids = [subissions_record_dict[i].id for i in submission_file_form_ids_options]
            mode = check_mode_value(submission_file_form_mode)

            file_data = submission_file(
                cid=content_option_dict[submission_file_form_cid_option].CID,
                submission_ids=ids,
                mode=mode,
            )

            if file_data:
                col2.download_button(
                    key="submission_file_download_button",
                    label="下載壓縮檔",
                    data=file_data,
                    file_name=f"{zip_filename if zip_filename else 'export_forder'}.zip",
                    mime="application/zip",
                )

            st.success(f"匯出檔案成功")

        except Exception as e:
            st.error(f"下載提交檔案失敗：{cid}，{e}")
    
    st.markdown('### 匯出提交紀錄')

    contest_files_form_cid_option = st.selectbox(
        "請選擇考區",
        options=content_option_dict,
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
    contest_files_submit = col1.button("匯出檔案", key="contest_files_submit")

    if contest_files_submit:
        try:
            cid = content_option_dict[contest_files_form_cid_option].CID
            mode = check_mode_value(contest_files_form_mode)
            file_data = contest_files(
                cid=cid,
                mode=mode,
            )

            if file_data:
                col2.download_button(
                    key="contest_files_download_button",
                    label="下載壓縮檔",
                    data=file_data,
                    file_name=f'{zip_filename if zip_filename else "export_forder"}.zip',
                    mime="application/zip",
                )
            else:
                st.error("輸入的題目 ID 有誤")

            st.success(f"匯出檔案成功")

        except Exception as e:
            st.error(f"匯出提交紀錄失敗：{e}")

if __name__ == "__main__":
    content_option_dict = get_content_options()
    submissions_page(content_option_dict)