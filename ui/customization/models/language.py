from typing import Optional, List

from pydantic import BaseModel


class Language(BaseModel):
    lid: str
    external_id: str
    name: str
    entrypoint: bool
    entry_point_description: Optional[str]
    allow_submit: bool
    allow_judge: bool
    timefactor: int
    extensions: Optional[List[str]]
    filter_files_passed_to_compiler_by_extension_list: Optional[bool]