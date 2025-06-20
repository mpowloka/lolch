from core.models.matchup import LaneMatchupReport, JungleMatchupReport, PowerLevelEntry, StyleComparisonEntry, JungleMatchupEntry
from core.models.threats import ThreatProjectionResult
from .interfaces import LLMAnalyzerInterface

class MockLLMAnalyzer(LLMAnalyzerInterface):
    def analyze_lane(self, context: dict) -> LaneMatchupReport:
        return LaneMatchupReport(
            champion_1=context.get("user_champion", "UnknownChamp1"),
            champion_2=context.get("enemy_champion", "UnknownChamp2"),
            power_levels=[
                PowerLevelEntry(level=i, status="Even", comment=f"Lorem ipsum at level {i}.") for i in range(1, 7)
            ],
            style_comparison=[
                StyleComparisonEntry(dimension="Sustain", ally="Lorem", enemy="Ipsum"),
                StyleComparisonEntry(dimension="Waveclear", ally="Dolor", enemy="Sit amet")
            ],
            tips=["Consectetur adipiscing elit.", "Sed do eiusmod tempor incididunt."]
        )

    def analyze_jungle(self, context: dict) -> JungleMatchupReport:
        return JungleMatchupReport(
            champion_1=context.get("ally_jungler", "UnknownJungler1"),
            champion_2=context.get("enemy_jungler", "UnknownJungler2"),
            entries=[
                JungleMatchupEntry(dimension="Clear Speed", ally="Lorem", enemy="Ipsum"),
                JungleMatchupEntry(dimension="Gank Threat", ally="Dolor", enemy="Sit amet")
            ]
        )

    def project_threats(self, context: dict) -> ThreatProjectionResult:
        return ThreatProjectionResult(
            sidelane_threats=["Championus Placeholderius"],
            teamfight_threats=["Ultimatus Mockius"]
        )
