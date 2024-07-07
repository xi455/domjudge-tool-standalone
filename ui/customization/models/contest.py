from typing import Optional

from pydantic import BaseModel


class Contest(BaseModel):
    cid: str
    shortname: str
    name: str
    activate: str
    start: str
    start_time_enabled: Optional[bool]
    scoreboard_freeze_time: Optional[str]
    end: str
    scoreboard_unfreeze_time: Optional[str]
    deactivate_time: Optional[str]
    record_balloons: Optional[bool]
    medals_enabled: Optional[bool]
    process_balloons: bool
    contest_open_to_all_teams: Optional[bool]
    enabled: Optional[bool]
    medals: Optional[str]
    public: bool
    teams: str
    problems: int