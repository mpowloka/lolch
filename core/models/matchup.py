from pydantic import BaseModel
from typing import Tuple, Dict, List
from core.models.literals import Comparison, LaningDimension, Strength, JungleDimension

class LaneMatchupReport(BaseModel):
    level_1: Tuple[Comparison, str]
    level_2: Tuple[Comparison, str]
    level_3: Tuple[Comparison, str]
    level_4: Tuple[Comparison, str]
    level_5: Tuple[Comparison, str]
    level_6: Tuple[Comparison, str]
    extra_spikes: Dict[int, Tuple[Comparison, str]]
    analysis: Dict[LaningDimension, Tuple[Strength, Strength, str]]
    extra_comments: List[str] = []

class JungleMatchupReport(BaseModel):
    analysis: Dict[JungleDimension, Tuple[Strength, Strength, str]]
    extra_comments: List[str] = []
