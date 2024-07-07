import streamlit as st

from customization.emails import send_user_accounts

from utils.check import login_required
from utils.web import get_example_data


st.set_page_config(page_title="寄送帳號頁面", page_icon="📄")

@login_required
def emails_page():
    st.sidebar.header("寄送帳號")
    st.title("寄送帳號")

    csv = get_example_data("templates/csv/send-email-example.csv")
    st.download_button(
        label="Download Example Send Email as CSV",
        data=csv,
        file_name="send-email-example.csv",
        mime="text/csv",
    )

    txt = get_example_data("templates/txt/body.txt")
    st.download_button(
        label="Download Template Example Data as TXT",
        data=txt,
        file_name="example_body.txt",
        mime="text/txt",
    )

    emails_csv = st.file_uploader("開啟帳號 .csv 檔案", type="csv")
    template_txt = st.file_uploader("模板目錄 .txt 檔案", type="txt")

    host = st.text_input(
        "主機位置",
        key="host",
        value=None,
        placeholder="請輸入主機位置",
    )

    port = st.text_input(
        "端口",
        key="port",
        value=None,
        placeholder="請輸入端口",
    )

    from_email = st.text_input(
        "From Email",
        key="from_email",
        value=None,
        placeholder="請輸入 From Email",
    )

    use_ssl = st.checkbox(
        "Use SSL",
        key="use_ssl",
        value=False,
    )

    timeout = st.number_input(
        "Timeout",
        key="timeout", 
        value=None,
        placeholder="請輸入 Timeout 時間",
    )

    username = st.text_input(
        "Username", 
        key="username", 
        value=None,
        placeholder="請輸入 Username",
    )

    password = st.text_input(
        "Gmail App 密碼",
        key="password",
        value=None,
        placeholder="請輸入 Password",
        type="password",
    )

    if st.button("寄送"):
        if emails_csv and template_txt:
            try:
                send_user_accounts(
                    file=emails_csv,
                    template_path=template_txt,
                    host=host,
                    port=port,
                    from_email=from_email,
                    use_ssl=use_ssl,
                    timeout=timeout,
                    username=username,
                    password=password,                
                )
                st.success(f"寄送成功")

            except Exception as e:
                st.error(f"錯誤：{e}")
        else:
            st.warning("請上傳 csv, txt 檔案")


if __name__ == "__main__":
    emails_page()