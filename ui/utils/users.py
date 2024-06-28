from enum import Enum


class UserRoles(str, Enum):
    Administrative_User = 1
    Jury_User = 2
    Team_User = 3
    Balloon_runner = 4
    Internal_System_Judgehost = 6
    API_reader = 9
    API_writer = 10
    Source_code_reader = 11
