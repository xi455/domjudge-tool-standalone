from typing import Optional

from pydantic import BaseModel


class Language(BaseModel):
    lid: Optional[str]
    external_id: Optional[str]
    name: Optional[str]
    entrypoint: Optional[bool]
    allow_submit: Optional[bool]
    allow_judge: Optional[bool]
    timefactor: Optional[int]
    extensions: Optional[str]