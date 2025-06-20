import requests
from .constants import RIOT_API_KEY, REGION

def get_live_game(puuid):
    url = f"https://{REGION}.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 404:
        return None  # User not currently in a game
    response.raise_for_status()
    return response.json()
