# 🧩 Full System Architecture with Pydantic Models

# VERY IMPORTANT
This document must be followed exactly and completely. Every interface, or model must be implemented with EXACTLY the name and location as specified here. Breaking any of these conventions will result in compromising the system.

# Core System Specification (Excluding Models & Interfaces)

This document outlines the specification and responsibilities for each system layer and module in the League of Legends Game Insight tool, excluding structured models and interface signatures.

---

## System Architecture Overview

```
[ Presentation Layer ]          ← HTML reports
        ↑
[ Application Layer ]           ← High-level coordination and control
     ↑        ↑
[ LLM Analysis Layer ]   [ Data Layer ]
```

Each layer handles a specific concern, ensuring modularity, ease of testing, and separation of responsibilities.

---

## Dependency Isolation

Each system module must include its own `requirements.txt`, e.g.:

- `llm_analysis/requirements.txt`

  ```
  pydantic>=2.0
  openai>=1.0
  ```

- `data_providers/requirements.txt`

  ```
  pydantic>=2.0
  requests>=2.31
  aiohttp>=3.8
  ```

> The shared model layer (`core/models/`) must remain dependency-free.

Additionally, a top-level development environment file should exist:

- `requirements-dev.txt`
  ```
  -r data_providers/requirements.txt
  -r llm_analysis/requirements.txt
  -r application/requirements.txt
  -r presentation/requirements.txt
  ```

This allows full integration testing and system-wide environment consistency.

---

## Folder Structure Summary

The following structure strictly aligns with the defined core models and their logical separation:

```
core/models/
  matchup.py
  cooldowns.py
  threats.py
  report.py
  raw_game_data.py
  context.py
  __init__.py

presentation/
  html_renderer.py
  interfaces.py
  templates/
  output/

data_providers/
  riot_client.py
  static_data.py
  interfaces.py

llm_analysis/
  gpt_lane_analyzer.py
  gpt_jungle_analyzer.py
  interfaces.py

application/
  game_analyzer.py
  interfaces.py

```

---

## Environment Tips

Each module should be independently installable and runnable:

```bash
cd llm_analysis && pip install -r requirements.txt
```

Avoid shared environment dependencies to maintain clarity and reproducibility.

---

## Model-to-File Mapping

To maintain separation of concerns and support isolated development, models are mapped into their respective files within `core/models/` as follows:

| File               | Contents                                                                                |
| ------------------ | --------------------------------------------------------------------------------------- |
| `literals.py`      | `PlayerRole`, `TeamSide`, `Comparison`, `Strength`, `LaningDimension `, `JungleDimension` |
| `champion_data.py` | `ChampionData`                                                                          |
| `runes.py`         | `Runes`                                                                                 |
| `game_data.py`     | `PlayerGameEntry`, `GameData`                                                           |
| `matchup.py`       | `LaneMatchupReport`, `JungleMatchupReport`                                              |
| `threats.py`       | `ThreatProjectionReport`                                                                |
| `cooldowns.py`     | `CooldownsComparisonReport`                                                             |
| `report.py`        | `FullMatchReport`                                                                       |

---

## Import Rules & Init Handling

To prevent ambiguity or environment-specific failures:

### `core/models/__init__.py` Requirements

Must re-export all key classes used across layers:

```python
from .literals import PlayerRole, TeamSide, Comparison, Strength, LaningDimension , JungleDimension
from .champion_data import ChampionData
from .runes import Runes
from .game_data import PlayerGameEntry, GameData
from .matchup import LaneMatchupReport, JungleMatchupReport
from .threats import ThreatProjectionReport
from .cooldowns import CooldownsComparisonReport
from .report import FullMatchReport
```

- Allows imports like:

```python
from core.models import CooldownsComparisonReport
from core.models import matchup
```

### Importing Rules

- Always use absolute imports relative to project root:

```python
from core.models.cooldowns import CooldownsComparisonReport
from data_providers.riot_client import RiotDataClient
```

- Never use relative imports like `from ..models import ...`
- Set `PYTHONPATH=.` when running scripts or tests to support import resolution

This ensures compatibility across scripts, tests, and LLM-generated modules.



### 🔹 Data Models

```python
PlayerRole = Literal["TOP", "JUNGLE", "MID", "BOTTOM", "SUPPORT"]
TeamSide = Literal["ALLY", "ENEMY"]
Comparison = Literal["Weaker", "Even", "Stronger"]
Strength = Literal["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]
LaningDimension  = Literal[
    "Sustain",
    "Waveclear",
    "All-in Threat",
    "Mana Demands",
    "Preferred Trading Pattern", # Poke / Burst / Long Trades
    "Roaming",
    "Scaling",
    "Teamfighting",
    "Preferred Macro Pattern" # Split pushing / Grouping / Assasinating
]

JungleDimension = Literal[
    "Clear Speed",
    "Early Gank Threat",
    "Scaling",
    "Teamfighting",
    "Preferred Macro Pattern", # Split pushing / Grouping / Assasinating
    "1v1 Threat",
    "2v2 Threat" # Considered for analysed user + his jungler vs enemy laner + their jungler
]

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

class RuneEntry(BaseModel):
    name: str
    shortDesc: str

class Runes(BaseModel):
    keystone: RuneEntry
    primary: List[RuneEntry]
    secondary: List[RuneEntry]
    shards: List[RuneEntry]

class SummonerSpell(BaseModel):
    name: str
    cooldown: List[float]
    description: str

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

    def get_user_entry(self) -> PlayerGameEntry: ...
    def get_lane_opponent_entry(self) -> PlayerGameEntry: ...
    def get_player(self, role: PlayerRole, team: TeamSide) -> PlayerGameEntry: ...
    def get_team(self, side: TeamSide) -> List[PlayerGameEntry]: ...

class LaneMatchupReport(BaseModel):
    # Power comparison at early levels 1–6
    level_1: Tuple[Comparison, str]
    level_2: Tuple[Comparison, str]
    level_3: Tuple[Comparison, str]
    level_4: Tuple[Comparison, str]
    level_5: Tuple[Comparison, str]
    level_6: Tuple[Comparison, str]

    # Extra power spikes at other levels (e.g., 9, 11, 13, 16)
    extra_spikes: Dict[int, Tuple[Comparison, str]]

    # Laning comparisons per dimension
    analysis: Dict[LaningDimension, Tuple[Strength, Strength, str]]

    # Optional: summary tags or tips
    extra_comments: List[str] = []

class JungleMatchupReport(BaseModel):
    # Jungle comparisons per dimension    
    analysis: Dict[JungleDimension, Tuple[Strength, Strength, str]]

    # Optional: summary tags or tips
    extra_comments: List[str] = []

class ThreatProjectionReport(BaseModel):
    sidelane_threats: Dict[str, str]
   """
   Dict mapping the champion name into the description of the side lane threat potential
   """

    teamfight_threats: Dict[str, str]
   """
   Dict mapping the champion name into the description of the teamfight threat potential
   """

class CooldownsComparisonReport(BaseModel):
    allyQ: Dict[str, List[float]]
    allyW: Dict[str, List[float]]
    allyE: Dict[str, List[float]]
    allyR: Dict[str, List[float]]

    enemyQ: Dict[str, List[float]]
    enemyW: Dict[str, List[float]]
    enemyE: Dict[str, List[float]]
    enemyR: Dict[str, List[float]]

    # Optional: suggestion on how to leverage cooldown differences and what threats to avoid with them
    cooldown_leverage_comment: str

class FullMatchReport(BaseModel):
    summoner_name: str
    lane: LaneMatchupReport
    jungle: JungleMatchupReport
    cooldowns: CooldownsComparisonReport
    threats: ThreatProjectionReport
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

class StaticDataProviderInterface(ABC):
    @abstractmethod
    def get_patch_version(self) -> str:
        """
        Returns the latest patch version from Riot CDN:
        - Used to construct all static Data Dragon URLs
        - Endpoint: /api/versions.json
        """

    @abstractmethod
    def get_all_champions(self) -> Dict[str, ChampionData]:
        """
        Returns a mapping of champion name to ChampionData object.
        - From /cdn/{version}/data/{lang}/champion.json
        """

    @abstractmethod
    def get_champion_data(self, champion_name: str) -> ChampionData:
        """
        Returns full stats and cooldowns for a single champion.
        - From /cdn/{version}/data/{lang}/champion/{CHAMPION_NAME}.json
        """

    @abstractmethod
    def get_all_runes(self) -> Dict[str, RuneEntry]:
        """
        Returns a mapping of rune name to RuneEntry object.
        - Parsed from /cdn/{version}/data/{lang}/runesReforged.json
        """

    @abstractmethod
    def get_spell_data(self) -> Dict[str, SummonerSpell]:
        """
        Returns a mapping of sumoner spell name to SummonerSpell object.
        - From /cdn/{version}/data/{lang}/summoner.json
        """
```

---

## 2️⃣ LLM Analysis Layer Interface

```python
class LLMAnalyzerInterface(ABC):
    @abstractmethod
    def get_lane_power_level(self, game_data: GameData, level: int) -> Tuple[Comparison, str]:
        """
        Return the power comparison and explanation at a specific level. (Usually 1-6 as they are required)
        """

    @abstractmethod
    def get_lane_extra_spikes(self, game_data: GameData) -> Dict[int, Tuple[Comparison, str]]:
        """
        Return optional extra spikes, usually at levels beyond 6 (e.g., 9, 11, 13, 16).
        """

    @abstractmethod
    def get_lane_style_entry(self, game_data: GameData, dimension: LaningDimension) -> Tuple[Strength, Strength, str]:
        """
        Return (ally strength, enemy strength, comment) for the given style dimension.
        """

    @abstractmethod
    def get_jungle_dimension_entry(self, game_data: GameData, dimension: JungleDimension) -> Tuple[Strength, Strength, str]:
        """
        Return (ally strength, enemy strength, comment) for the given jungle dimension.
        """

    @abstractmethod
    def get_teamfight_threats(self, game_data: GameData) -> Dict[str, str]:
        """
        Return a mapping of champion name → threat description in teamfights.
        """

    @abstractmethod
    def get_sidelane_threats(self, game_data: GameData) -> Dict[str, str]:
        """
        Return a mapping of champion name → threat description in 1v1 sidelane matchups.
        """

    @abstractmethod
    def get_cooldowns_leverage_suggestion(self, game_data: GameData) -> str:
        """
        Return a mapping of champion name → threat description in 1v1 sidelane matchups.
        """

    @abstractmethod
    def start_context_window(self) -> None:
        """
        Called before feeding multiple items to the LLM. Used to initialize state or reset memory buffers.
        """

    @abstractmethod
    def end_context_window(self) -> None:
        """
        Called after LLM input sequence completes. Used to flush, reset, or finalize any temporary state.
        """
```

---

## 3️⃣ Application Layer Interface

```python
class GameInsightAnalyzerInterface(ABC):
    def analyze_lane_matchup(self, game_data: GameData) -> LaneMatchupReport:
        """
        Analyze a lane matchup using structured game data.
        - Compares early level spikes, runes, and trading patterns.
        - Returns structured lane matchup report.
        """

    def analyze_jungle_matchup(self, game_data: GameData) -> JungleMatchupReport:
        """
        Analyze the jungle matchup from game context:
        - Includes clear speed, gank potential, synergy with top lane
        - Based on champion data and summoner setup
        """

    def analyze_threats(self, game_data: GameData) -> ThreatProjectionReport:
        """
        Projects mid-to-late game threats:
        - Identifies 1v1 sidelane threats and teamfight carry potential
        - Uses full team composition, roles and champion scaling
        """

    def analyze_cooldowns(self, game_data: GameData) -> CooldownsComparisonReport:
        """
        Returns per-level ability cooldowns for user and lane opponent:
        - Structured for visual comparison (Q/W/E/R spells)
        """
```

---

## 4️⃣ Presentation Layer Interface

```python
class ReportRendererInterface(ABC):
    @abstractmethod
    def render_html_report(self, report_data: FullMatchReport, output_path: Path) -> None:
        """
        Render a styled HTML report file from a complete match analysis.
        The file will be written to the given output path.
        """

    @abstractmethod
    def get_output_filename(self, summoner_name: str, timestamp: str) -> str:
        """
        Return a filename string using summoner name and timestamp.
        Format: 'report_{name}_{YYYY-MM-DD_HH-MM}.html'
        """
```

---