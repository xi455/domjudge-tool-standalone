from enum import Enum


class UserRoles(Enum):
    ADMINISTRATIVE_USER = ("Administrative User", 1)
    JURY_USER = ("Jury User", 2)
    TEAM_USER = ("Team Member", 3)
    BALLOON_RUNNER = ("Balloon runner", 4)
    INTERNAL_SYSTEM_JUDGEHOST = ("(Internal/System) Judgehost", 6)
    API_READER = ("API reader", 9)
    API_WRITER = ("API writer", 10)
    SOURCE_CODE_READER = ("Source code reader", 11)

    @classmethod
    def get_user_roles_values(cls):
        return {role.value[0]: role.value[1] for role in cls}