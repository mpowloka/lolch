from pydantic import BaseModel
from core.models.matchup import LaneMatchupReport, JungleMatchupReport
from core.models.cooldowns import CooldownsComparisonReport
from core.models.threats import ThreatProjectionReport

class FullMatchReport(BaseModel):
    summoner_name: str
    lane: LaneMatchupReport
    jungle: JungleMatchupReport
    cooldowns: CooldownsComparisonReport
    threats: ThreatProjectionReport
