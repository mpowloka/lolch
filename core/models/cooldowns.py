from pydantic import BaseModel
from typing import Dict, List

class CooldownTable(BaseModel):
    spells: Dict[str, Dict[str, List[float]]]
