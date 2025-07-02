from application.interfaces import GameInsightAnalyzerInterface
from core.models import (
    GameData,
    LaneMatchupReport,
    JungleMatchupReport,
    ThreatProjectionReport,
    CooldownsComparisonReport,
    LaningDimension,
    JungleDimension,
)


class GameInsightAnalyzer(GameInsightAnalyzerInterface):
    def __init__(self, llm):
        self.llm = llm

    def start_insight_session(self) -> None:
        self.llm.start_context_window()

    def end_insight_session(self) -> None:
        self.llm.end_context_window()

    def analyze_lane_matchup(self, game_data: GameData) -> LaneMatchupReport:
        level_keys = [1, 2, 3, 4, 5, 6]
        level_data = {
            f"level_{i}": self.llm.get_lane_power_level(game_data, i)
            for i in level_keys
        }

        extra_spikes = self.llm.get_lane_extra_spikes(game_data)
        style_analysis = {
            dim: self.llm.get_lane_style_entry(game_data, dim)
            for dim in LaningDimension.__args__
        }

        return LaneMatchupReport(
            **level_data,
            extra_spikes=extra_spikes,
            analysis=style_analysis,
            extra_comments=[]
        )

    def analyze_jungle_matchup(self, game_data: GameData) -> JungleMatchupReport:
        analysis = {
            dim: self.llm.get_jungle_dimension_entry(game_data, dim)
            for dim in JungleDimension.__args__
        }
        return JungleMatchupReport(analysis=analysis, extra_comments=[])

    def analyze_threats(self, game_data: GameData) -> ThreatProjectionReport:
        sidelane_threats = self.llm.get_sidelane_threats(game_data)
        teamfight_threats = self.llm.get_teamfight_threats(game_data)
        return ThreatProjectionReport(
            sidelane_threats=sidelane_threats,
            teamfight_threats=teamfight_threats
        )

    def analyze_cooldowns(self, game_data: GameData) -> CooldownsComparisonReport:
        user = game_data.get_user_entry()
        opponent = game_data.get_lane_opponent_entry()

        return CooldownsComparisonReport(
            allyQ={user.summoner_name: user.champion.q_cooldowns},
            allyW={user.summoner_name: user.champion.w_cooldowns},
            allyE={user.summoner_name: user.champion.e_cooldowns},
            allyR={user.summoner_name: user.champion.r_cooldowns},
            enemyQ={opponent.summoner_name: opponent.champion.q_cooldowns},
            enemyW={opponent.summoner_name: opponent.champion.w_cooldowns},
            enemyE={opponent.summoner_name: opponent.champion.e_cooldowns},
            enemyR={opponent.summoner_name: opponent.champion.r_cooldowns},
            cooldown_leverage_comment=self.llm.get_cooldowns_leverage_suggestion(game_data)
        )
