# game_data_assembler.py
from data_providers.interfaces import GameDataInterface
from data_providers.riot_client import RiotApiClient
from data_providers.static_data import StaticDataProvider
from data_providers._internal.mapping import map_raw_to_game_data
from core.models import GameData

class GameDataAssembler(GameDataInterface):
    def __init__(self):
        self.riot = RiotApiClient()
        self.static = StaticDataProvider()

    def get_live_game_info(self, game_name: str, tag_line: str) -> GameData:
        puuid = self.riot.get_puuid(game_name, tag_line)
        raw = self.riot.get_active_game(puuid)
        return map_raw_to_game_data(raw, game_name, self.static)

    def get_historical_game(self, match_id: str, game_name: str, tag_line: str) -> GameData:
        raw = self.riot.get_match_details(match_id)
        return map_raw_to_game_data(raw, game_name, self.static)

    def get_recent_game_ids(self, game_name: str, tag_line: str, count: int = 10) -> list[str]:
        puuid = self.riot.get_puuid(game_name, tag_line)
        return self.riot.get_match_ids(puuid, count)
