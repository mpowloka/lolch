from pydantic import BaseModel
from typing import List

class SummonerSpell(BaseModel):
    name: str
    cooldown: List[float]
    description: str