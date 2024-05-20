import pkg_resources
import streamlit as st

from domjudge_tool_cli.commands.emails import send_user_accounts

from utils.check import login_required

st.set_page_config(page_title="創建帳號頁面", page_icon="📄")

@st.cache_data
def convert_df(pkg_path):
    path = pkg_resources.resource_filename("domjudge_tool_cli", pkg_path)

    with open(path, "r", encoding="utf-8") as f:
        csv = f.read()

    return csv


@login_required
def emails_page():
    st.sidebar.header("創建帳號")
    st.title("創建帳號")

    csv = convert_df("templates/csv/import-users-teams.csv")
    st.download_button(
        label="Download Example Data as CSV",
        data=csv,
        file_name="example_users_teams.csv",
        mime="text/csv",
    )

    email_form = st.form("email_form")

    emails_csv = email_form.file_uploader("開啟帳號 .csv 檔案", type="csv")

    template_dir = email_form.text_input(
        "模板目錄",
        key="template_dir",
        value=None,
        placeholder="請輸入模板目錄",
    )

    host = email_form.text_input(
        "網址連結",
        key="host",
        value=None,
        placeholder="請輸入網址連結",
    )

    port = email_form.number_input(
        "端口",
        key="port",
        value=None,
        placeholder="請輸入端口",
    )

    from_email = email_form.text_input(
        "From Email",
        key="from_email",
        value=None,
        placeholder="請輸入 From Email",
    )

    use_ssl = email_form.checkbox(
        "Use SSL",
        key="use_ssl",
        value=False,
    )

    # format = email_form.text_input(
    #     "Format",
    #     key="format",
    #     value=None,
    #     placeholder="請輸入 Format",
    # )
    timeout = email_form.number_input(
        "Timeout",
        key="timeout", 
        value=None,
        placeholder="請輸入 Timeout 時間",
    )

    username = email_form.text_input(
        "Username", 
        key="username", 
        value=None,
        placeholder="請輸入 Username",
    )

    password = email_form.text_input(
        "Password",
        key="password",
        value=None,
        placeholder="請輸入 Password",
        type="password",
    )

    submit = email_form.form_submit_button("寄送")

    if submit:
        try:
            send_user_accounts(
                emails_csv=emails_csv,
                template_dir=template_dir,
                host=host,
                port=port,
                from_email=from_email,
                use_ssl=use_ssl,
                format=format,
                timeout=timeout,
                username=username,
                password=password,                
            )
            st.success(f"寄送成功")

        except Exception as e:
            st.error(f"錯誤：{e}")


if __name__ == "__main__":
    emails_page()
