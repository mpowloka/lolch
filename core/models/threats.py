from pydantic import BaseModel
from typing import Dict

class ThreatProjectionReport(BaseModel):
    sidelane_threats: Dict[str, str]
    teamfight_threats: Dict[str, str]
