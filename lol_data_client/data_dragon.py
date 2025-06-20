import requests

def get_latest_patch_version():
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    versions = requests.get(url).json()
    return versions[0]

def get_data_dragon_static(version):
    base = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US"
    return {
        "champions": requests.get(f"{base}/champion.json").json(),
        "summoner_spells": requests.get(f"{base}/summoner.json").json(),
        "runes": requests.get(f"{base}/runesReforged.json").json()
    }
