from core.models import GameData, LaningDimension, JungleDimension

class PromptFactory:
    def build_lane_power_prompt(self, game_data: GameData, level: int) -> str:
        user = game_data.get_user_entry()
        opponent = game_data.get_lane_opponent_entry()
        return (
            f"Compare power at level {level} between {user.champion.name} and {opponent.champion.name}. "
            f"Summarize who is stronger and why, considering base stats, abilities, runes, and power spikes."
        )

    def build_lane_style_prompt(self, game_data: GameData, dimension: LaningDimension) -> str:
        user = game_data.get_user_entry()
        opponent = game_data.get_lane_opponent_entry()
        return (
            f"Compare {dimension} between {user.champion.name} and {opponent.champion.name}. "
            f"Rate their strength in this dimension and explain your reasoning."
        )

    def build_extra_spikes_prompt(self, game_data: GameData) -> str:
        user = game_data.get_user_entry()
        opponent = game_data.get_lane_opponent_entry()
        return (
            f"Identify any additional power spikes beyond level 6 for {user.champion.name} versus {opponent.champion.name}. "
            f"Explain what makes those spikes impactful."
        )

    def build_jungle_prompt(self, game_data: GameData, dimension: JungleDimension) -> str:
        ally_jungle = game_data.get_player("JUNGLE", "ALLY")
        enemy_jungle = game_data.get_player("JUNGLE", "ENEMY")
        return (
            f"Compare {dimension} between junglers {ally_jungle.champion.name} and {enemy_jungle.champion.name}. "
            f"Rate both sides and describe their comparative strengths."
        )

    def build_teamfight_prompt(self, game_data: GameData) -> str:
        return (
            "Evaluate each champion's potential impact in teamfights. "
            "Provide one sentence per champion summarizing their threat level or role in 5v5 scenarios."
        )

    def build_sidelane_prompt(self, game_data: GameData) -> str:
        return (
            "Evaluate each champion's threat level in 1v1 sidelane duels post-laning phase. "
            "Explain which champions are dangerous in those isolated matchups."
        )

    def build_cooldown_prompt(self, game_data: GameData) -> str:
        user = game_data.get_user_entry()
        opponent = game_data.get_lane_opponent_entry()
        return (
            f"Given ability cooldowns for {user.champion.name} and {opponent.champion.name}, "
            f"suggest ways to exploit timing differences in lane trades or all-ins."
        )
