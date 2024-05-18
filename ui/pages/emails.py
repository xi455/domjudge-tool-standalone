import streamlit as st

from domjudge_tool_cli.commands import emails

from utils.login import login_required

st.set_page_config(page_title="創建帳號頁面", page_icon="📄")


@login_required
def emails_page():
    st.sidebar.header("創建帳號")
    st.title("創建帳號")

    email_form = st.form("email_form")

    emails_csv = st.file_uploader("開啟帳號 .csv 檔案", type="csv")

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

    port = email_form.text_input(
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

    format = email_form.text_input(
        "Format",
        key="format",
        value=None,
        placeholder="請輸入 Format",
    )
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

    submit = email_form.form_submit_button("登入")

    if submit:
        try:
            emails.send_user_accounts(
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
