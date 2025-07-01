from abc import ABC, abstractmethod
from core.models import GameData, ChampionData, RuneEntry, SummonerSpell
from typing import Dict, List

class GameDataInterface(ABC):
    @abstractmethod
    def get_live_game_info(self, game_name: str, tag_line: str) -> GameData: ...

    @abstractmethod
    def get_historical_game(self, match_id: str, game_name: str, tag_line: str) -> GameData: ...

    @abstractmethod
    def get_recent_game_ids(self, game_name: str, tag_line: str, count: int = 10) -> list[str]: ...

class RiotApiClientInterface(ABC):
    @abstractmethod
    def get_puuid(self, game_name: str, tag_line: str) -> str: ...

    @abstractmethod
    def get_active_game(self, puuid: str) -> dict: ...

    @abstractmethod
    def get_match_ids(self, puuid: str, count: int = 10) -> List[str]: ...

    @abstractmethod
    def get_match_details(self, match_id: str) -> dict: ...

class StaticDataProviderInterface(ABC):
    @abstractmethod
    def get_patch_version(self) -> str: ...

    @abstractmethod
    def get_all_champions(self) -> Dict[str, ChampionData]: ...

    @abstractmethod
    def get_champion_data(self, champion_name: str) -> ChampionData: ...

    @abstractmethod
    def get_all_runes(self) -> Dict[str, RuneEntry]: ...

    @abstractmethod
    def get_spell_data(self) -> Dict[str, SummonerSpell]: ...