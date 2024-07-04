import asyncio

from enum import Enum

from customization._submissions import get_submissions
from utils.check import login_required
from utils.web import get_config


class ModeValue(Enum):
    MODE_FIRST = ("選擇一：team_name/problem_name/submission_file", 1)
    MODE_SECOND = ("選擇二：problem_name/team_name/submission_file", 2)
    TEAM_THIRTH = ("選擇三：contest_id/submission_file", 3)

    @classmethod
    def get_mode_values(cls):
        return {role.value[0]: role.value[1] for role in cls}


@login_required
def get_submissions_record(content_option_dict, contest_name, language_option_dict=None, language_name=None):
    """
    Retrieves the submissions record for a given contest and language.

    Args:
        content_option_dict (dict): A dictionary containing the contest options.
        contest_name (str): The name of the contest.
        language_option_dict (dict, optional): A dictionary containing the language options. Defaults to None.
        language_name (str, optional): The name of the language. Defaults to None.
    """

    lid = language_name
    cid = content_option_dict[contest_name].cid
    if language_name:
        lid = language_option_dict[language_name].lid

    client = get_config()
    return asyncio.run(get_submissions(client, cid, lid))