import json
from pathlib import Path

_PREFS_FILE = Path("./my user data.txt")

if not _PREFS_FILE.exists():
    raise FileNotFoundError("Missing 'my user data.txt' in project root.")

with _PREFS_FILE.open("r") as f:
    lines = f.readlines()
    prefs = {}
    for line in lines:
        if ":" in line:
            key, val = line.strip().split(":", 1)
            prefs[key.strip()] = val.strip().strip('"')

RIOT_API_TOKEN = prefs.get("token")
DEFAULT_GAME_NAME = prefs.get("gameName")
DEFAULT_TAG_LINE = prefs.get("tagLine")
REGION = prefs.get("region", "europe")
SERVER = prefs.get("server", "euw1")

if not RIOT_API_TOKEN:
    raise EnvironmentError("Riot API token not found in user data.")

def get_headers() -> dict:
    return {"X-Riot-Token": RIOT_API_TOKEN}

def get_cdn_url(version: str, lang: str, endpoint: str) -> str:
    return f"https://ddragon.leagueoflegends.com/cdn/{version}/data/{lang}/{endpoint}"

def get_cdn_asset_url(path: str) -> str:
    return f"https://ddragon.leagueoflegends.com/cdn/img/{path}"