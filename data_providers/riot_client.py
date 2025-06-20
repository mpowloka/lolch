import requests
from core.models.raw_game_data import RawLiveGameData, ParticipantInfo
from data_providers.interfaces import RiotDataClientInterface

class RiotAPIClient(RiotDataClientInterface):
    def __init__(self, token: str, region: str, server: str):
        self.token = token
        self.region = region
        self.server = server
        self.headers = {"X-Riot-Token": self.token}

    def get_puuid(self, game_name: str, tag_line: str) -> str:
        url = f"https://{self.region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()["puuid"]

    def get_summoner_id(self, puuid: str) -> str:
        url = f"https://{self.server}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()["id"]

    def get_live_game_info(self, puuid: str) -> RawLiveGameData:
        url = f"https://{self.server}.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        data = response.json()

        participants = []
        for p in data["participants"]:
            participants.append(ParticipantInfo(
                summoner_name=p["summonerName"],
                team_id=p["teamId"],
                champion_name=p["championName"],
                perks=p["perks"],
                summoner_spells=[str(p["summoner1Id"]), str(p["summoner2Id"])],
                position=p.get("teamPosition", "UNKNOWN")
            ))

        return RawLiveGameData(
            game_id=str(data["gameId"]),
            participants=participants
        )