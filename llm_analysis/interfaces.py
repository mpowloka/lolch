from abc import ABC, abstractmethod
from core.models.matchup import LaneMatchupReport, JungleMatchupReport
from core.models.threats import ThreatProjectionResult

class LLMAnalyzerInterface(ABC):
    @abstractmethod
    def analyze_lane(self, context: dict) -> LaneMatchupReport:
        pass

    @abstractmethod
    def analyze_jungle(self, context: dict) -> JungleMatchupReport:
        pass

    @abstractmethod
    def project_threats(self, context: dict) -> ThreatProjectionResult:
        pass