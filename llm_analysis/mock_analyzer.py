from typing import Tuple, Dict
from llm_analysis.interfaces import LLMAnalyzerInterface
from core.models import (
    GameData,
    Comparison,
    Strength,
    LaningDimension,
    JungleDimension
)

class MockLLMAnalyzer(LLMAnalyzerInterface):
    def start_context_window(self) -> None:
        self._context_active = True

    def end_context_window(self) -> None:
        self._context_active = False

    def get_lane_power_level(self, game_data: GameData, level: int) -> Tuple[Comparison, str]:
        levels = ["Weaker", "Even", "Stronger"]
        return levels[level % 3], f"Mock reason for level {level}"

    def get_lane_extra_spikes(self, game_data: GameData) -> Dict[int, Tuple[Comparison, str]]:
        return {
            9: ("Stronger", "Mock spike at 9"),
            11: ("Even", "Mock spike at 11"),
            13: ("Weaker", "Mock spike at 13"),
            16: ("Stronger", "Mock spike at 16")
        }

    def get_lane_style_entry(self, game_data: GameData, dimension: LaningDimension) -> Tuple[Strength, Strength, str]:
        return ("Moderate", "Strong", f"Mock analysis for {dimension}")

    def get_jungle_dimension_entry(self, game_data: GameData, dimension: JungleDimension) -> Tuple[Strength, Strength, str]:
        return ("Weak", "Very Strong", f"Mock jungle analysis for {dimension}")

    def get_teamfight_threats(self, game_data: GameData) -> Dict[str, str]:
        return {
            player.champion.name: "Mock teamfight threat description"
            for player in game_data.players
        }

    def get_sidelane_threats(self, game_data: GameData) -> Dict[str, str]:
        return {
            player.champion.name: "Mock sidelane threat description"
            for player in game_data.players
        }

    def get_cooldowns_leverage_suggestion(self, game_data: GameData) -> str:
        return "Mock cooldowns leverage insight based on ability timing and trade windows."
