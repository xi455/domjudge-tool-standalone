from typing import Optional

from pydantic import BaseModel


class Language(BaseModel):
    LID: Optional[str]
    externalID: Optional[str]
    name: Optional[str]
    entrypoint: Optional[bool]
    allowsubmit: Optional[bool]
    allowjudge: Optional[bool]
    timefactor: Optional[int]
    extensions: Optional[str]