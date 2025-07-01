from pydantic import BaseModel
from typing import Dict, List

class CooldownsComparisonReport(BaseModel):
    allyQ: Dict[str, List[float]]
    allyW: Dict[str, List[float]]
    allyE: Dict[str, List[float]]
    allyR: Dict[str, List[float]]
    enemyQ: Dict[str, List[float]]
    enemyW: Dict[str, List[float]]
    enemyE: Dict[str, List[float]]
    enemyR: Dict[str, List[float]]
    cooldown_leverage_comment: str
