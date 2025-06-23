# 🧩 Full System Architecture with Pydantic Models

## VERY IMPORTANT
This document must be followed exactly and completely. Every interface, or model must be implemented with EXACTLY the name and location as specified here. Breaking any of these conventions will result in compromising the system.

This document defines the complete, interface-driven architecture for the LoL Game Insight system, including:
- Layered responsibilities
- Interfaces between layers
- Shared structured data models using `pydantic`
- Integration point for LLM-based subjective analysis

---

## 📚 System Layers

```
[ Presentation Layer ]
    ↑
[ Application Layer (Analyzers) ]
    ↑
[ LLM Analysis Layer ]   ← Subjective evaluation (LLM-based)
    ↑
[ Data Layer (Riot API + Data Dragon) ]
```

---

## 📦 Unified Data Models (`core/models/`)

All data exchanged across layers must use these structured `pydantic` models.

---

### 🔹 Basic Literals

```python
PlayerRole = Literal["TOP", "JUNGLE", "MID", "BOTTOM", "SUPPORT"]
TeamSide = Literal["ALLY", "ENEMY"]
```

### 🔹 ChampionData

```python
class ChampionData(BaseModel):
    name: str

    # Base stats at level 1
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

    # Per-level gains
    hp_per_level: float
    mp_per_level: float
    armor_per_level: float
    mr_per_level: float
    ad_per_level: float
    as_per_level: float

    # Cooldowns per ability (Q/W/E/R)
    q_cooldowns: List[float]
    w_cooldowns: List[float]
    e_cooldowns: List[float]
    r_cooldowns: List[float]
```

### 🔹 Runes

```python
class Runes(BaseModel):
    keystone: str
    primary: List[str]
    secondary: List[str]
    shards: List[str]
```

### 🔹 GameData

```python
class GameData(BaseModel):
    game_id: str
    summoner_name: str
    players: List[PlayerGameEntry]
    user_role: PlayerRole

    def get_user_entry(self) -> PlayerGameEntry: ...
    def get_lane_opponent_entry(self) -> PlayerGameEntry: ...
    def get_player(self, role: PlayerRole, team: TeamSide) -> PlayerGameEntry: ...
    def get_team(self, side: TeamSide) -> List[PlayerGameEntry]: ...
```

### 🔹 ChampionData

```python
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
```

---

## 1️⃣ Data Layer Interface

```python
class GameDataInterface(ABC):
    def get_live_game_info(self, game_name: str, tag_line: str) -> GameData:
        """Returns structured metadata for a live game (if the user is in one)."""

    def get_historical_game(self, match_id: str, game_name: str, tag_line: str) -> GameData:
        """Returns structured metadata for a past match for the given player."""

    def get_recent_game_ids(self, game_name: str, tag_line: str, count: int = 10) -> list[str]:
        """Returns the N most recent match IDs for the given player."""


class RiotApiClientInterface(ABC):  # Raw Riot API access
    def get_puuid(self, game_name: str, tag_line: str) -> str:
        """Resolve Riot ID to account PUUID."""

    def get_active_game(self, puuid: str) -> dict:
        """
        Returns raw live game data from Riot Spectator API:
        - gameId, gameMode, gameType, participants (with championId, summonerName, perks, teamId, etc.)
        - Used for /lol/spectator/v5/active-games/by-summoner/{puuid}
        """

    def get_match_ids(self, puuid: str, count: int = 10) -> List[str]:
        """
        Returns a list of recent match IDs from Match API:
        - Uses /lol/match/v5/matches/by-puuid/{puuid}/ids
        - Response is a list of match ID strings
        """

    def get_match_details(self, match_id: str) -> dict:
        """
        Returns full match data from Match API:
        - Includes game info and participant data with championId, teamId, stats, perks
        - Used for /lol/match/v5/matches/{matchId}
        """

class StaticDataProviderInterface(ABC):  # Data Dragon access
    def get_patch_version(self) -> str:
        """
        Returns the latest patch version from Riot CDN:
        - Used to construct all static Data Dragon URLs
        - Endpoint: /api/versions.json
        """

    def get_all_champions(self) -> dict:
        """
        Returns summary metadata for all champions:
        - Name, ID, tags (roles), image assets
        - From /cdn/{version}/data/{lang}/champion.json

        Example Response:
        {
            "data": {
                "Aatrox": {
                    "id": "Aatrox",
                    "key": "266",
                    "name": "Aatrox",
                    "tags": ["Fighter", "Tank"],
                    "image": {"full": "Aatrox.png"},
                    ...
                },
                ...
            }
        }
        """

    def get_champion_data(self, champion_name: str) -> ChampionData:
        """Returns full stats and cooldowns for a champion."""

    def get_all_runes(self) -> Dict[int, str]:
        """
        Returns a mapping of rune ID to rune name:
        - Parsed from /cdn/{version}/data/{lang}/runesReforged.json
        - Includes keystones, primaries, secondaries, and stat shards
        """

    def get_spell_data(self) -> dict:
        """
        Returns metadata for all summoner spells:
        - ID, name, cooldown, description
        - From /cdn/{version}/data/{lang}/summoner.json

        Example Response:
        {
            "data": {
                "SummonerFlash": {
                    "id": "SummonerFlash",
                    "name": "Flash",
                    "cooldown": 300,
                    "description": "Teleports your champion a short distance...",
                    ...
                },
                ...
            }
        }
        """
```

---

## 2️⃣ LLM Analysis Layer Interface

```python

```

---

## 3️⃣ Application Layer Interface

```python

```

---

## 4️⃣ Presentation Layer Interface

```python

```

---

## 📘 `__init__.py` Convention for `core.models`

Each submodule in `core/models/` (e.g., `matchup.py`, `cooldowns.py`) defines logically grouped data models. To improve import clarity and ensure compatibility with all layers:

- A single `__init__.py` file must re-export key models from each submodule.
- This supports:
  - `from core.models import CooldownTable`
  - `from core.models.matchup import LaneMatchupReport`
  - `from core.models import matchup` (namespace access)

All developers and agents must treat the `__init__.py` file as the **authoritative import surface** of shared models.

---

## 📦 Dependency Management

To maintain modularity and ensure distributed or LLM-based implementation is seamless, **each system module must manage its own dependencies explicitly**.

### 📦 Per-Module Requirements (Mandatory)

Each top-level folder (`llm_analysis/`, `data_providers/`, `application/`, `presentation/`, etc.) **must include its own**:
- `requirements.txt` file (mandatory)

Example for `llm_analysis/requirements.txt`:

```txt
pydantic>=2.0
openai>=1.0
```

Example for `data_providers/requirements.txt`:

```txt
pydantic>=2.0
requests>=2.31
aiohttp>=3.8
```

### 📘 Shared Models

The shared `core/models/` module:
- Must **not define its own requirements.txt**
- Must remain importable by all other modules

Each module is responsible for installing whatever `pydantic`, typing, or helper libraries it uses to consume these models.

---

## 🔁 Environment Setup

Each module must be independently installable using:

```bash
pip install -r requirements.txt
```

From its own folder.

This:
- Reduces coupling
- Encourages separation of concerns
- Enables parallel and sandboxed development by LLMs or contributors

---

## 🧪 Test Structure (Recommended)

Directory structure for testing mirrors the production module layout:

```
tests/
├── test_data_providers/
├── test_llm_analysis/
├── test_application/
├── test_presentation/
```

Use `pytest` or `unittest`, and test:
- Data parsing and retrieval
- LLM mock results
- HTML rendering logic
- Model validations
