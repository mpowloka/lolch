from data_providers.riot_client import RiotAPIClient
from data_providers.static_data import DataDragonClient

token = "RGAPI-e2126839-d146-4b52-a98d-13e483c1baca"
region = "europe"
server = "euw1"
game_name = "Cpt Szumi"
tag_line = "EUNE"

riot_client = RiotAPIClient(token=token, region=region, server=server)
static_client = DataDragonClient()

print("--- Testing Riot API ---")
try:
    puuid = riot_client.get_puuid(game_name, tag_line)
    print("PUUID:", puuid)

    summoner_id = riot_client.get_summoner_id(puuid)
    print("Summoner ID:", summoner_id)

    game_data = riot_client.get_live_game_info(puuid)
    print("Live Game Participants:", [p.summoner_name for p in game_data.participants])
except Exception as e:
    print("Error fetching Riot API data:", e)

print("\n--- Testing Data Dragon ---")
try:
    version = static_client.get_patch_version()
    print("Latest Patch:", version)

    champions = static_client.get_all_champions()
    print("Number of Champions:", len(champions["data"]))

    aatrox_data = static_client.get_champion_data("Aatrox")
    print("Aatrox Lore Snippet:", aatrox_data["data"]["Aatrox"]["lore"][:100], "...")
except Exception as e:
    print("Error fetching Data Dragon data:", e)