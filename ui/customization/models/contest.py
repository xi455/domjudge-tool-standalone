from typing import Optional

from pydantic import BaseModel


class Contest(BaseModel):
    CID: str
    name: str
    shortname: str
    activate: str
    start: str
    end: str
    processballoons: bool
    public: bool
    teams: str
    problems: int