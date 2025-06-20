import requests
from .constants import RIOT_API_KEY, REGIONAL_ROUTING

def get_match_history(puuid, count=5):
    base_url = f"https://{REGIONAL_ROUTING}.api.riotgames.com/lol/match/v5/matches"
    match_ids_url = f"{base_url}/by-puuid/{puuid}/ids?start=0&count={count}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    match_ids = requests.get(match_ids_url, headers=headers).json()

    match_data = []
    for match_id in match_ids:
        match_url = f"{base_url}/{match_id}"
        match_resp = requests.get(match_url, headers=headers)
        if match_resp.ok:
            match_data.append(match_resp.json())
    return match_data
