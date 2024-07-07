import logging
import streamlit as st

from pydantic import ValidationError

from customization.submissions import submission_file, contest_files
from customization.options import content_options
from customization import exceptions as cust_exceptions

from utils.check import login_required
from utils.submissions import get_submissions_record, ModeValue


@login_required
def submissions_page():
    mode_options_dict = ModeValue.get_mode_values()
    content_option_dict = content_options()

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
        try:
            subissions_record_dict = get_submissions_record(content_option_dict, contest_name)
        
        except ValidationError as e:
            logger.error(f"ValidationError: {e}")
            st.error(f"無法取得提交紀錄，請檢查 網址連結 SSL 是否設定正確")

    if "subissions_record_dict" in locals():
        submission_file_form_ids_options = st.multiselect(
        "選擇提交紀錄",
        subissions_record_dict,)

    submission_file_form_mode = st.selectbox(
        "輸出路徑樣式選擇",
        options=mode_options_dict.keys(),
        key="submission_file_form_mode",
    )

    zip_filename = st.text_input(
        "ZIP 檔案名稱",
        key="submission_file_form_zip_filename",
        value=None,
        placeholder="請輸入 ZIP 檔案名稱",
    )

    col1, col2, col3, col4 = st.columns([2, 3, 3, 4])


    if col1.button("匯出檔案", key="submission_file_submit"):
        try:
            ids = [subissions_record_dict[i].id for i in submission_file_form_ids_options]
            mode = mode_options_dict.get(submission_file_form_mode)

            file_data = submission_file(
                cid=content_option_dict[submission_file_form_cid_option].cid,
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

            logger.info(f"Export Submissions Success")
            st.success(f"匯出檔案成功")

        except cust_exceptions.SubmissionNotFoundException as e:
            logger.error(f"SubmissionNotFoundException: {e}")
            st.error(e)

        except Exception as e:
            logger.error(f"Download Submissions Error, Exception: {e}")
            st.error(f"下載提交檔案失敗")
    
    st.markdown('### 匯出提交紀錄')

    contest_files_form_cid_option = st.selectbox(
        "請選擇考區",
        options=content_option_dict,
        key="contest_files_form_cid_option",
    )

    contest_files_form_mode = st.selectbox(
        "輸出路徑樣式選擇",
        options=mode_options_dict.keys(),
        key="contest_files_form_mode",
    )

    zip_filename = st.text_input(
        "ZIP 檔案名稱",
        key="contest_files_form_zip_filename",
        value=None,
        placeholder="請輸入 ZIP 檔案名稱",
    )

    col1, col2, col3, col4 = st.columns([3, 3, 4, 4])
    if col1.button("匯出檔案", key="contest_files_submit"):
        try:
            cid = content_option_dict[contest_files_form_cid_option].cid
            mode = mode_options_dict.get(contest_files_form_mode)
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

            logger.info(f"Export Submissions Success")
            st.success(f"匯出檔案成功")

        except cust_exceptions.SubmissionNotFoundException as e:
            logger.error(f"SubmissionNotFoundException: {e}")
            st.error(e)

        except Exception as e:
            logger.error(f"Submissions Error, Exception: {e}")
            st.error(f"匯出提交紀錄失敗")

if __name__ == "__main__":
    logger = logging.getLogger("standalone_logger")
    logger.info("GET /submissions")

    submissions_page()