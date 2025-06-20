from pydantic import BaseModel
from typing import Literal
from typing import List

class PowerLevelEntry(BaseModel):
    level: int
    status: Literal["Stronger", "Weaker", "Even"]
    comment: str

class StyleComparisonEntry(BaseModel):
    dimension: str
    ally: str
    enemy: str

class LaneMatchupReport(BaseModel):
    champion_1: str
    champion_2: str
    power_levels: List[PowerLevelEntry]
    style_comparison: List[StyleComparisonEntry]
    tips: List[str] = []

class JungleMatchupEntry(BaseModel):
    dimension: str
    ally: str
    enemy: str

class JungleMatchupReport(BaseModel):
    champion_1: str
    champion_2: str
    entries: List[JungleMatchupEntry]
