from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from enum import Enum

from string import Template
from typing import Any, Dict, List

from domjudge_tool_cli.utils.email.helper import FileType, EmailContext


class CustomFileType(str, Enum):
    TEXT = ".txt"
    HTML = ".html"


class CustomEmailContext(EmailContext):
    subject_template: Template
    body_template: Template
    body_file_type: FileType

    def __init__(
        self,
        subject_template: str,
        body_template: str
    ):
        self.subject_template = Template(subject_template)
        self.body_template = Template(body_template)
        self.body_file_type = CustomFileType.TEXT

    def render_subject(self, **kwargs) -> str:
        return self.subject_template.substitute(**kwargs)

    def render_body(self, **kwargs) -> str:
        return self.body_template.substitute(**kwargs)

    def mime(
        self,
        from_email: str,
        to_address: List[str],
        **kwargs: Dict[str, Any],
    ) -> MIMEText:
        _, domain = from_email.split("@")
        mail_content_type = "html" if self.body_file_type == FileType.HTML else "plain"
        subject = self.render_subject(**kwargs)
        content = self.render_body(**kwargs)
        mime = MIMEText(content, mail_content_type, "utf-8")
        mime["Subject"] = subject
        mime["From"] = from_email
        mime["Date"] = formatdate(localtime=True)
        mime["Message-ID"] = make_msgid(domain=domain)
        mime["To"] = ",".join(to_address)

        return mime
