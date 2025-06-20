from pydantic import BaseModel
from typing import List, Dict

class ParticipantInfo(BaseModel):
    summoner_name: str
    team_id: int
    champion_name: str
    perks: Dict[str, List[int]]
    summoner_spells: List[str]
    position: str

class RawLiveGameData(BaseModel):
    game_id: str
    participants: List[ParticipantInfo]
