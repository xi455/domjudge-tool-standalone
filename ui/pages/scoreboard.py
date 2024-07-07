import logging
import streamlit as st

from customization.scoreboard import export
from customization.options import content_options

from utils.check import login_required

@login_required
def scoreboard_page():
    content_option_dict = content_options()

    st.set_page_config(page_title="匯出分數頁面", page_icon="📄")
    st.sidebar.header("匯出分數")
    st.title("匯出分數")

    contest_name = st.selectbox(
        "請選擇考區",
        options=content_option_dict,
        key="contest_files_form_cid_option",
    )

    filename = st.text_input(
        "檔案名稱",
        key="filename",
        value= "export",
        placeholder="請輸入檔案名稱",
    )

    col1, col2, col3, col4 = st.columns([2, 2, 4, 4])
    if col1.button("匯出分數"):
        try:
            cid = content_option_dict[contest_name].cid

            csv_data = export(cid)
            col2.download_button(
                label="下載檔案",
                data=csv_data,
                file_name=f'{filename if filename else "score"}.csv',
                mime="text/csv",
            )

            logger.info(f"Export Scoreboard Success")
            st.success(f"匯出檔案成功")

        except Exception as e:
            logger.error(f"Export Scoreboard Error, Exception: {e}")
            st.error("匯出失敗")

if __name__ == "__main__":
    logger = logging.getLogger("standalone_logger")
    logger.info("GET /scoreboard")

    scoreboard_page()