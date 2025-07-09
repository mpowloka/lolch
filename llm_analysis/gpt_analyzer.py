from typing import Tuple, Dict
from llm_analysis.interfaces import LLMAnalyzerInterface
from core.models import (
    GameData,
    Comparison,
    Strength,
    LaningDimension,
    JungleDimension
)
from llm_analysis.prompts.prompt_factory import PromptFactory
from llm_analysis.langchain_client.llm_client import LLMClient
from llm_analysis.context.context_window import ContextWindow
from llm_analysis.parsing.parser import (
    parse_comparison_output,
    parse_strength_output,
    parse_threat_output,
    parse_cooldown_tip
)

class GPTLLMAnalyzer(LLMAnalyzerInterface):
    def __init__(self):
        self.context = ContextWindow()
        self.prompter = PromptFactory()
        self.llm = LLMClient()  # Will internally use langchain-community

    def start_context_window(self) -> None:
        self.context.clear()

    def end_context_window(self) -> None:
        self.context.clear()

    def get_lane_power_level(self, game_data: GameData, level: int) -> Tuple[Comparison, str]:
        prompt = self.prompter.build_lane_power_prompt(game_data, level)
        response = self.llm.call(prompt)
        return parse_comparison_output(response)

    def get_lane_extra_spikes(self, game_data: GameData) -> Dict[int, Tuple[Comparison, str]]:
        prompt = self.prompter.build_extra_spikes_prompt(game_data)
        response = self.llm.call(prompt)
        spikes = {}
        for line in response.split("\n"):
            if ":" in line:
                lvl_str, detail = line.split(":", 1)
                try:
                    level = int(lvl_str.strip())
                    spikes[level] = parse_comparison_output(detail.strip())
                except Exception:
                    continue
        return spikes

    def get_lane_style_entry(self, game_data: GameData, dimension: LaningDimension) -> Tuple[Strength, Strength, str]:
        prompt = self.prompter.build_lane_style_prompt(game_data, dimension)
        response = self.llm.call(prompt)
        return parse_strength_output(response)

    def get_jungle_dimension_entry(self, game_data: GameData, dimension: JungleDimension) -> Tuple[Strength, Strength, str]:
        prompt = self.prompter.build_jungle_prompt(game_data, dimension)
        response = self.llm.call(prompt)
        return parse_strength_output(response)

    def get_teamfight_threats(self, game_data: GameData) -> Dict[str, str]:
        prompt = self.prompter.build_teamfight_prompt(game_data)
        response = self.llm.call(prompt)
        return parse_threat_output(response)

    def get_sidelane_threats(self, game_data: GameData) -> Dict[str, str]:
        prompt = self.prompter.build_sidelane_prompt(game_data)
        response = self.llm.call(prompt)
        return parse_threat_output(response)

    def get_cooldowns_leverage_suggestion(self, game_data: GameData) -> str:
        prompt = self.prompter.build_cooldown_prompt(game_data)
        response = self.llm.call(prompt)
        return parse_cooldown_tip(response)
