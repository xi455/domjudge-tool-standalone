import streamlit as st

from utils.check import login_required
from customization.scoreboard import export
from customization.submissions import get_content_options


@login_required
def scoreboard_page():
    st.set_page_config(page_title="匯出分數頁面", page_icon="📄")
    st.sidebar.header("匯出分數")
    st.title("匯出分數")

    contest_name = st.selectbox(
        "請選擇考區",
        options=st.session_state["content_option"],
        key="contest_files_form_cid_option",
    )

    filename = st.text_input(
        "檔案名稱",
        key="filename",
        value= "export",
        placeholder="請輸入檔案名稱",
    )

    col1, col2, col3, col4 = st.columns([2, 2, 4, 4])
    export_button = col1.button("匯出分數")

    if export_button:
        try:
            cid = st.session_state["content_option"][contest_name].CID

            csv_data = export(cid)
            col2.download_button(
                label="下載檔案",
                data=csv_data,
                file_name=f'{filename if filename else "score"}.csv',
                mime="text/csv",
            )

        except Exception as e:
            st.error("匯出失敗：", e)

if __name__ == "__main__":
    st.session_state["content_option"] = get_content_options()
    scoreboard_page()