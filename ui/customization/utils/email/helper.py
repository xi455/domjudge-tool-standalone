from enum import Enum
from string import Template

from domjudge_tool_cli.utils.email.helper import EmailContext


class CustomFileType(str, Enum):
    TEXT = ".txt"
    HTML = ".html"


class CustomEmailContext(EmailContext):
    def __init__(self, subject_template: str, body_template: str):
        self.subject_template = Template(subject_template)
        self.body_template = Template(body_template)
        self.body_file_type = CustomFileType.TEXT
