from typing import Optional

from pydantic import BaseModel


class Contest(BaseModel):
    cid: str
    name: str
    shortname: str
    activate: str
    start: str
    end: str
    process_balloons: bool
    public: bool
    teams: str
    problems: int