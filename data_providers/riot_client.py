from data_providers.interfaces import RiotApiClientInterface
from data_providers._internal.config import REGION, SERVER, get_headers
from data_providers._internal.http_client import HttpClient
from urllib.parse import quote

class RiotApiClient(RiotApiClientInterface):
    def __init__(self):
        self.http = HttpClient()
        self.base_general = f"https://{SERVER}.api.riotgames.com"
        self.base_regional = f"https://{REGION}.api.riotgames.com"

    def get_puuid(self, game_name: str, tag_line: str) -> str:
        encoded_name = quote(game_name)
        encoded_tag = quote(tag_line)
        url = f"{self.base_regional}/riot/account/v1/accounts/by-riot-id/{encoded_name}/{encoded_tag}"
        return self.http.get(url, headers=get_headers())["puuid"]

    def get_active_game(self, puuid: str) -> dict:
        url = f"{self.base_general}/lol/spectator/v5/active-games/by-summoner/{puuid}"
        return self.http.get(url, headers=get_headers())

    def get_match_ids(self, puuid: str, count: int = 10) -> list[str]:
        url = f"{self.base_regional}/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
        return self.http.get(url, headers=get_headers())

    def get_match_details(self, match_id: str) -> dict:
        url = f"{self.base_regional}/lol/match/v5/matches/{match_id}"
        return self.http.get(url, headers=get_headers())