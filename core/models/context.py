from pydantic import BaseModel
from typing import List, Dict

class LaneAnalysisContext(BaseModel):
    user_champion: str
    enemy_champion: str
    user_runes: List[int]
    enemy_runes: List[int]
    user_summoners: List[str]
    enemy_summoners: List[str]
    level_1_stats: Dict[str, float]
    lane_role: str  # e.g. "TOP", "MID", "BOTTOM", "SUPPORT"

class JungleAnalysisContext(BaseModel):
    ally_jungler: str
    enemy_jungler: str
    ally_champion_top: str
    enemy_champion_top: str
    ally_runes: List[int]
    enemy_runes: List[int]
