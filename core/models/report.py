from pydantic import BaseModel
from core.models.matchup import LaneMatchupReport, JungleMatchupReport
from core.models.cooldowns import CooldownTable
from core.models.threats import ThreatProjectionResult

class FullMatchReport(BaseModel):
    summoner_name: str
    lane: LaneMatchupReport
    jungle: JungleMatchupReport
    cooldowns: CooldownTable
    threats: ThreatProjectionResult
