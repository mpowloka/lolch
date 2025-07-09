from abc import ABC, abstractmethod
from typing import Dict, Tuple
from core.models.game_data import GameData
from core.models.literals import Comparison, JungleDimension, LaningDimension, Strength

class LLMAnalyzerInterface(ABC):
    @abstractmethod
    def get_lane_power_level(self, game_data: GameData, level: int) -> Tuple[Comparison, str]:
        """
        Return the power comparison and explanation at a specific level. (Usually 1-6 as they are required)
        """

    @abstractmethod
    def get_lane_extra_spikes(self, game_data: GameData) -> Dict[int, Tuple[Comparison, str]]:
        """
        Return optional extra spikes, usually at levels beyond 6 (e.g., 9, 11, 13, 16).
        """

    @abstractmethod
    def get_lane_style_entry(self, game_data: GameData, dimension: LaningDimension) -> Tuple[Strength, Strength, str]:
        """
        Return (ally strength, enemy strength, comment) for the given style dimension.
        """

    @abstractmethod
    def get_jungle_dimension_entry(self, game_data: GameData, dimension: JungleDimension) -> Tuple[Strength, Strength, str]:
        """
        Return (ally strength, enemy strength, comment) for the given jungle dimension.
        """

    @abstractmethod
    def get_teamfight_threats(self, game_data: GameData) -> Dict[str, str]:
        """
        Return a mapping of champion name → threat description in teamfights.
        """

    @abstractmethod
    def get_sidelane_threats(self, game_data: GameData) -> Dict[str, str]:
        """
        Return a mapping of champion name → threat description in 1v1 sidelane matchups.
        """

    @abstractmethod
    def get_cooldowns_leverage_suggestion(self, game_data: GameData) -> str:
        """
        Return a mapping of champion name → threat description in 1v1 sidelane matchups.
        """

    @abstractmethod
    def start_context_window(self) -> None:
        """
        Called before feeding multiple items to the LLM. Used to initialize state or reset memory buffers.
        """

    @abstractmethod
    def end_context_window(self) -> None:
        """
        Called after LLM input sequence completes. Used to flush, reset, or finalize any temporary state.
        """