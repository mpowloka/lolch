from abc import ABC, abstractmethod
from core.models import matchup, cooldowns, threats
from core.models.raw_game_data import RawLiveGameData


class GameInsightAnalyzerInterface(ABC):
    @abstractmethod
    def analyze_lane_matchup(self, user_champ: str, enemy_champ: str) -> matchup.LaneMatchupReport:
        pass

    @abstractmethod
    def analyze_jungle_matchup(self, ally_jg: str, enemy_jg: str) -> matchup.JungleMatchupReport:
        pass

    @abstractmethod
    def analyze_threats(self, full_game_data: RawLiveGameData) -> threats.ThreatProjectionResult:
        pass

    @abstractmethod
    def get_cooldown_table(self, champ1: str, champ2: str) -> cooldowns.CooldownTable:
        pass
