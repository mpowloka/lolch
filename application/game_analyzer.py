from core.models import matchup, cooldowns, threats
from core.models.context import LaneAnalysisContext, JungleAnalysisContext
from core.models.threats import ThreatProjectionInput
from core.models.raw_game_data import RawLiveGameData
from application.interfaces import GameInsightAnalyzerInterface
from data_providers.interfaces import RiotDataClientInterface, StaticDataProviderInterface
from llm_analysis.interfaces import LLMAnalyzerInterface


class GameInsightAnalyzer(GameInsightAnalyzerInterface):
    def __init__(self,
                 riot_client: RiotDataClientInterface,
                 static_data: StaticDataProviderInterface,
                 llm_analyzer: LLMAnalyzerInterface):
        self.riot = riot_client
        self.static = static_data
        self.llm = llm_analyzer

    def analyze_lane_matchup(self, user_champ: str, enemy_champ: str) -> matchup.LaneMatchupReport:
        champ1_data = self.static.get_champion_data(user_champ)
        champ2_data = self.static.get_champion_data(enemy_champ)

        context = LaneAnalysisContext(
            user_champion=user_champ,
            enemy_champion=enemy_champ,
            user_runes=[],
            enemy_runes=[],
            user_summoners=[],
            enemy_summoners=[],
            level_1_stats={
                'user_hp': champ1_data['stats']['hp'],
                'enemy_hp': champ2_data['stats']['hp']
            },
            lane_role="TOP"
        )
        return self.llm.analyze_lane(context.model_dump())

    def analyze_jungle_matchup(self, ally_jg: str, enemy_jg: str) -> matchup.JungleMatchupReport:
        context = JungleAnalysisContext(
            ally_jungler=ally_jg,
            enemy_jungler=enemy_jg,
            ally_champion_top="",
            enemy_champion_top="",
            ally_runes=[],
            enemy_runes=[],
        )
        return self.llm.analyze_jungle(context.model_dump())

    def analyze_threats(self, full_game_data: RawLiveGameData) -> threats.ThreatProjectionResult:
        blue_team = [p.champion_name for p in full_game_data.participants if p.team_id == 100]
        red_team = [p.champion_name for p in full_game_data.participants if p.team_id == 200]
        roles = {p.champion_name: p.position for p in full_game_data.participants}

        context = ThreatProjectionInput(
            blue_team=blue_team,
            red_team=red_team,
            roles=roles
        )
        return self.llm.project_threats(context.model_dump())

    def get_cooldown_table(self, champ1: str, champ2: str) -> cooldowns.CooldownTable:
        data1 = self.static.get_champion_data(champ1)
        data2 = self.static.get_champion_data(champ2)

        def extract_cd(cdata):
            return {
                spell['id'][-1]: spell['cooldown']
                for spell in cdata['spells']
            }

        return cooldowns.CooldownTable(
            spells={
                champ1: extract_cd(data1),
                champ2: extract_cd(data2)
            }
        )
