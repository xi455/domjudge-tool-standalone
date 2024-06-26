from typing import Optional

from tablib import Dataset

from domjudge_tool_cli.models import CreateUser

from customization.utils.email import helper, smtp

def send_user_accounts(
    file: Optional[object],
    template_path: Optional[object],
    host: Optional[str] = "localhost",
    port: Optional[int] = 25,
    from_email: Optional[str] = "noreply@localhost",
    use_ssl: Optional[bool] = False,
    format: Optional[str] = "csv",
    timeout: Optional[int] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
):
    input_file = file.read()
    input_file = input_file.decode("utf-8").split("\n") # 二進制轉換成字符串

    file_content = template_path.read()
    text_content = file_content.decode("utf-8").split("\n") # 二進制轉換成字符串
    
    subject_template = text_content[0].replace('subject: ', '').strip()
    body_template = '\n'.join(text_content[2:]).replace('body: ', '', 1).strip()

    dataset = Dataset().load(input_file, format=format)
    context = helper.CustomEmailContext(subject_template, body_template)
    _, domain = from_email.split("@")
    connection = smtp.CustomSMTP(
        host,
        port,
        use_ssl,
        timeout,
        username,
        password,
    )

    connection.open()
    for item in dataset.dict:
        item["email"] = None if not item.get("email") else item["email"]

        user = CreateUser(**item)
        to_email = f"{user.username}@{domain}" if not user.email else user.email
        connection.send_message(from_email, [to_email], context, **item)

    connection.close()
