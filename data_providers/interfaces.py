from abc import ABC, abstractmethod
from core.models.raw_game_data import RawLiveGameData

class RiotDataClientInterface(ABC):
    @abstractmethod
    def get_puuid(self, game_name: str, tag_line: str) -> str: ...

    @abstractmethod
    def get_live_game_info(self, puuid: str) -> RawLiveGameData: ...

    @abstractmethod
    def get_summoner_id(self, puuid: str) -> str: ...

    @abstractmethod
    def get_recent_match_ids(self, puuid: str, count: int = 1) -> list[str]: ...

    @abstractmethod
    def get_match_data(self, match_id: str) -> dict: ...

    @abstractmethod
    def extract_match_participant_summary(self, match_data: dict, puuid: str) -> dict: ...


class StaticDataProviderInterface(ABC):
    @abstractmethod
    def get_champion_data(self, champion_name: str) -> dict: ...

    @abstractmethod
    def get_all_champions(self) -> dict: ...

    @abstractmethod
    def get_spell_data(self) -> dict: ...

    @abstractmethod
    def get_item_data(self) -> dict: ...

    @abstractmethod
    def get_rune_data(self) -> dict: ...

    @abstractmethod
    def get_patch_version(self) -> str: ...