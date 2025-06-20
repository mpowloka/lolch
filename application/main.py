from application.game_analyzer import GameInsightAnalyzer
from core.models import matchup, cooldowns, threats, raw_game_data
from typing import Dict, List

from llm_analysis.interfaces import LLMAnalyzerInterface
class MockLLMAnalyzer(LLMAnalyzerInterface):
    def analyze_lane(self, context: dict) -> matchup.LaneMatchupReport:
        return matchup.LaneMatchupReport(
            champion_1=context['user_champion'],
            champion_2=context['enemy_champion'],
            power_levels=[
                matchup.PowerLevelEntry(level=i, status="Even", comment="Mocked power level") for i in range(1, 7)
            ],
            style_comparison=[
                matchup.StyleComparisonEntry(dimension="Sustain", ally="High", enemy="Medium")
            ],
            tips=["Use your Q smartly"]
        )

    def analyze_jungle(self, context: dict) -> matchup.JungleMatchupReport:
        return matchup.JungleMatchupReport(
            champion_1=context['ally_jungler'],
            champion_2=context['enemy_jungler'],
            entries=[
                matchup.JungleMatchupEntry(dimension="Clear Speed", ally="Fast", enemy="Slow")
            ]
        )

    def project_threats(self, context: dict) -> threats.ThreatProjectionResult:
        return threats.ThreatProjectionResult(
            sidelane_threats=["Zed"],
            teamfight_threats=["Malphite"]
        )

from data_providers.interfaces import StaticDataProviderInterface
class MockStaticData(StaticDataProviderInterface):
    def get_champion_data(self, champion_name: str) -> dict:
        return {
            "id": champion_name,
            "stats": {"hp": 600},
            "spells": [
                {"id": f"{champion_name}Q", "cooldown": [12, 11, 10, 9, 8]},
                {"id": f"{champion_name}W", "cooldown": [16, 15, 14, 13, 12]},
                {"id": f"{champion_name}E", "cooldown": [10, 9, 8, 7, 6]},
                {"id": f"{champion_name}R", "cooldown": [100, 80, 60]},
            ]
        }

    def get_all_champions(self): return {}
    def get_spell_data(self): return {}
    def get_item_data(self): return {}
    def get_rune_data(self): return {}
    def get_patch_version(self): return "14.12.1"

def main():
    analyzer = GameInsightAnalyzer(
        riot_client=None,
        static_data=MockStaticData(),
        llm_analyzer=MockLLMAnalyzer()
    )

    lane = analyzer.analyze_lane_matchup("Aatrox", "Darius")
    jungle = analyzer.analyze_jungle_matchup("LeeSin", "JarvanIV")
    cooldown = analyzer.get_cooldown_table("Aatrox", "Darius")

    fake_game = raw_game_data.RawLiveGameData(
        game_id="12345",
        participants=[
            raw_game_data.ParticipantInfo(
                summoner_name="Cpt Szumi",
                team_id=100,
                champion_name="Aatrox",
                perks={},
                summoner_spells=[],
                position="TOP"
            ),
            raw_game_data.ParticipantInfo(
                summoner_name="EnemyTop",
                team_id=200,
                champion_name="Darius",
                perks={},
                summoner_spells=[],
                position="TOP"
            )
        ]
    )

    threats_result = analyzer.analyze_threats(fake_game)

    print("Lane Matchup:", lane)
    print("\nJungle Matchup:", jungle)
    print("\nCooldown Table:", cooldown)
    print("\nThreat Projections:", threats_result)

if __name__ == '__main__':
    main()
