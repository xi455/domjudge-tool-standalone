from typing import Optional

from pydantic import BaseModel


class Category(BaseModel):
    id: str
    icpc_id: Optional[str]
    sortorder: str
    name: str
    color: Optional[str]
    teams: int
    visible: bool
    allow_self_registration: bool