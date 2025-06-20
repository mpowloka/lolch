from .account import get_account_info, get_summoner_info
from .live_game import get_live_game
from .match_history import get_match_history
from .formatter import format_output
from datetime import datetime

def extract_players_from_live(live_data):
    return [
        {
            "summonerName": p["summonerName"],
            "team": p["teamId"],
            "championId": p["championId"],
            "summonerSpells": [p["spell1Id"], p["spell2Id"]],
            "runes": p["perks"]
        }
        for p in live_data["participants"]
    ]

def extract_players_from_history(match_data, puuid):
    players = []
    for match in match_data:
        for p in match["info"]["participants"]:
            if p["puuid"] == puuid:
                players.append({
                    "summonerName": p["summonerName"],
                    "team": p["teamId"],
                    "championId": p["championId"],
                    "summonerSpells": [p["summoner1Id"], p["summoner2Id"]],
                    "runes": {
                        "primaryStyle": p["perks"]["styles"][0],
                        "secondaryStyle": p["perks"]["styles"][1]
                    }
                })
    return players

def get_user_data(username, tag, include_matches=True):
    puuid = get_account_info(username, tag)
    live_data = get_live_game(puuid)

    if live_data:
        game_type = "live"
        players = extract_players_from_live(live_data)
    elif include_matches:
        game_type = "match_history"
        match_data = get_match_history(puuid)
        players = extract_players_from_history(match_data, puuid)
    else:
        return None

    timestamp = datetime.utcnow().isoformat()
    return format_output(game_type, timestamp, players)
