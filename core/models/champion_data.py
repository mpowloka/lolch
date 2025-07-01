from pydantic import BaseModel
from typing import List

class ChampionData(BaseModel):
    name: str

    base_hp: float
    base_hp_regen: float
    base_mp: float
    base_mp_regen: float
    base_armor: float
    base_mr: float
    base_ad: float
    base_as: float
    base_movespeed: float
    base_range: float

    hp_per_level: float
    mp_per_level: float
    armor_per_level: float
    mr_per_level: float
    ad_per_level: float
    as_per_level: float

    q_cooldowns: List[float]
    w_cooldowns: List[float]
    e_cooldowns: List[float]
    r_cooldowns: List[float]