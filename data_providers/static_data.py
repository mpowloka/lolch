import requests
from data_providers.interfaces import StaticDataProviderInterface

class DataDragonClient(StaticDataProviderInterface):
    def __init__(self, lang: str = "en_US"):
        self.base_url = "https://ddragon.leagueoflegends.com"
        self.lang = lang
        self.version = self.get_patch_version()

    def get_patch_version(self) -> str:
        url = f"{self.base_url}/api/versions.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()[0]  # Latest version

    def _localized_url(self, path: str) -> str:
        return f"{self.base_url}/cdn/{self.version}/data/{self.lang}/{path}"

    def get_all_champions(self) -> dict:
        url = self._localized_url("champion.json")
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_champion_data(self, champion_name: str) -> dict:
        url = self._localized_url(f"champion/{champion_name}.json")
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["data"][champion_name]

    def get_spell_data(self) -> dict:
        url = self._localized_url("summoner.json")
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_item_data(self) -> dict:
        url = self._localized_url("item.json")
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_rune_data(self) -> dict:
        url = self._localized_url("runesReforged.json")
        response = requests.get(url)
        response.raise_for_status()
        return response.json()