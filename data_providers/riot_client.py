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
    
    def get_recent_match_ids(self, puuid: str, count: int = 1) -> list[str]:
        url = f"https://{self.region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_match_data(self, match_id: str) -> dict:
        url = f"https://{self.region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def extract_match_participant_summary(self, match_data: dict, puuid: str) -> dict:
        participants = match_data["info"]["participants"]
        user = next(p for p in participants if p["puuid"] == puuid)
        user_team_id = user["teamId"]
        user_role = user["teamPosition"]

        # Find enemy laner in same role
        enemy = next(
            p for p in participants
            if p["teamPosition"] == user_role and p["teamId"] != user_team_id
        )

        # Find junglers on both teams
        ally_jungler = next(
            p["championName"] for p in participants
            if p["teamId"] == user_team_id and p["teamPosition"] == "JUNGLE"
        )
        enemy_jungler = next(
            p["championName"] for p in participants
            if p["teamId"] != user_team_id and p["teamPosition"] == "JUNGLE"
        )

        # Team compositions
        blue_team = [p["championName"] for p in participants if p["teamId"] == 100]
        red_team = [p["championName"] for p in participants if p["teamId"] == 200]
        roles = {p["championName"]: p["teamPosition"] for p in participants}

        return {
            "user_champion": user["championName"],
            "enemy_champion": enemy["championName"],
            "ally_jungler": ally_jungler,
            "enemy_jungler": enemy_jungler,
            "blue_team": blue_team,
            "red_team": red_team,
            "roles": roles,
            "summoner_name": user["summonerName"]
        }

