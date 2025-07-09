from core.models import GameData

class ContextWindow:
    def __init__(self):
        self._buffer = {}

    def set(self, key: str, value: str) -> None:
        self._buffer[key] = value

    def get(self, key: str) -> str | None:
        return self._buffer.get(key)

    def clear(self) -> None:
        self._buffer.clear()

    def preload_from_game(self, game_data: GameData) -> None:
        # Optional: cache things like champ names, roles, spell names etc.
        user = game_data.get_user_entry()
        opponent = game_data.get_lane_opponent_entry()
        self.set("user_champ", user.champion.name)
        self.set("opponent_champ", opponent.champion.name)
        self.set("user_role", user.role)
        self.set("summoner_name", user.summoner_name)
