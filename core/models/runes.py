from pydantic import BaseModel
from typing import List

class RuneEntry(BaseModel):
    name: str
    shortDesc: str

class Runes(BaseModel):
    keystone: RuneEntry
    primary: List[RuneEntry]
    secondary: List[RuneEntry]
    shards: List[RuneEntry]