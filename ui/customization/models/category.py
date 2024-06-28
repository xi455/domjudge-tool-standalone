from typing import Optional

from pydantic import BaseModel


class Category(BaseModel):
    ID: str
    sortorder: Optional[str]
    name: str
    color: Optional[str]
    teams: Optional[int]
    visible: bool
    allow_self_registration: bool