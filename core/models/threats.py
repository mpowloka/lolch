from pydantic import BaseModel
from typing import List, Dict

class ThreatProjectionInput(BaseModel):
    blue_team: List[str]
    red_team: List[str]
    roles: Dict[str, str]  # champion_name → role

class ThreatProjectionResult(BaseModel):
    sidelane_threats: List[str]
    teamfight_threats: List[str]
