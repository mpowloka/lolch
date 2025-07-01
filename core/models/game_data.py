from pydantic import BaseModel
from typing import List
from core.models.champion_data import ChampionData
from core.models.runes import Runes
from core.models.literals import PlayerRole, TeamSide

class PlayerGameEntry(BaseModel):
    summoner_name: str
    champion: ChampionData
    runes: Runes
    summoner_spells: List[str]
    role: PlayerRole
    team: TeamSide

class GameData(BaseModel):
    game_id: str
    summoner_name: str
    players: List[PlayerGameEntry]
    user_role: PlayerRole

    def get_user_entry(self) -> PlayerGameEntry:
        return next(p for p in self.players if p.summoner_name == self.summoner_name)

    def get_lane_opponent_entry(self) -> PlayerGameEntry:
        user = self.get_user_entry()
        return next(p for p in self.players if p.role == user.role and p.team != user.team)

    def get_player(self, role: PlayerRole, team: TeamSide) -> PlayerGameEntry:
        return next(p for p in self.players if p.role == role and p.team == team)

    def get_team(self, side: TeamSide) -> List[PlayerGameEntry]:
        return [p for p in self.players if p.team == side]