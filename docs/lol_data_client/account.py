import requests
from .constants import RIOT_API_KEY, REGION, REGIONAL_ROUTING

def get_account_info(game_name, tag_line):
    url = f"https://{REGIONAL_ROUTING}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["puuid"]

def get_summoner_info(puuid):
    url = f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["id"]
