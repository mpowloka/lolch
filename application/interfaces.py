from abc import ABC, abstractmethod
from core.models import (
    GameData,
    LaneMatchupReport,
    JungleMatchupReport,
    ThreatProjectionReport,
    CooldownsComparisonReport,
)

class GameInsightAnalyzerInterface(ABC):
    @abstractmethod
    def start_insight_session(self) -> None:
        pass

    @abstractmethod
    def end_insight_session(self) -> None:
        pass

    @abstractmethod
    def analyze_lane_matchup(self, game_data: GameData) -> LaneMatchupReport:
        pass

    @abstractmethod
    def analyze_jungle_matchup(self, game_data: GameData) -> JungleMatchupReport:
        pass

    @abstractmethod
    def analyze_threats(self, game_data: GameData) -> ThreatProjectionReport:
        pass

    @abstractmethod
    def analyze_cooldowns(self, game_data: GameData) -> CooldownsComparisonReport:
        pass
