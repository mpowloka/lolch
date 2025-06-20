# 🧩 Full System Architecture with Pydantic Models

This document defines the complete, interface-driven architecture for the LoL Game Insight system, including:
- Layered responsibilities
- Interfaces between layers
- Shared structured data models using `pydantic`
- Integration point for LLM-based subjective analysis

---

## 📚 System Layers

```plaintext
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

### 🔹 PowerLevelEntry

```python
from pydantic import BaseModel, Literal

class PowerLevelEntry(BaseModel):
    level: int
    status: Literal["Stronger", "Weaker", "Even"]
    comment: str
```

---

### 🔹 StyleComparisonEntry

```python
class StyleComparisonEntry(BaseModel):
    dimension: str  # e.g. "Sustain", "Waveclear"
    ally: str
    enemy: str
```

---

### 🔹 LaneMatchupReport

```python
from typing import List

class LaneMatchupReport(BaseModel):
    champion_1: str
    champion_2: str
    power_levels: List[PowerLevelEntry]
    style_comparison: List[StyleComparisonEntry]
    tips: List[str] = []
```

---

### 🔹 JungleMatchupEntry

```python
class JungleMatchupEntry(BaseModel):
    dimension: str
    ally: str
    enemy: str
```

---

### 🔹 JungleMatchupReport

```python
class JungleMatchupReport(BaseModel):
    champion_1: str
    champion_2: str
    entries: List[JungleMatchupEntry]
```

---

### 🔹 CooldownTable

```python
from typing import Dict, List

class CooldownTable(BaseModel):
    spells: Dict[str, Dict[str, List[float]]]
```

---

### 🔹 ThreatProjectionResult

```python
class ThreatProjectionResult(BaseModel):
    sidelane_threats: List[str]
    teamfight_threats: List[str]
```

---

### 🔹 FullMatchReport

```python
class FullMatchReport(BaseModel):
    summoner_name: str
    lane: LaneMatchupReport
    jungle: JungleMatchupReport
    cooldowns: CooldownTable
    threats: ThreatProjectionResult
```

---

### 🔹 RawLiveGameData

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

### 🔹 ThreatProjectionInput

```python
class ThreatProjectionInput(BaseModel):
    blue_team: List[str]
    red_team: List[str]
    roles: Dict[str, str]  # champion_name → role
```

---

### 🔹 LaneAnalysisContext

```python
class LaneAnalysisContext(BaseModel):
    user_champion: str
    enemy_champion: str
    user_runes: List[int]
    enemy_runes: List[int]
    user_summoners: List[str]
    enemy_summoners: List[str]
    level_1_stats: Dict[str, float]
    lane_role: str  # e.g. "TOP", "MID", "BOTTOM", "SUPPORT"
```

---

### 🔹 JungleAnalysisContext

```python
class JungleAnalysisContext(BaseModel):
    ally_jungler: str
    enemy_jungler: str
    ally_champion_top: str
    enemy_champion_top: str
    ally_runes: List[int]
    enemy_runes: List[int]
```


## 1️⃣ Data Layer Interface

```python
from abc import ABC, abstractmethod
from core.models.raw_game_data import RawLiveGameData

class RiotDataClientInterface(ABC):
    def get_puuid(self, game_name: str, tag_line: str) -> str:
        """Resolve Riot ID (game name + tagline) to globally unique player ID (PUUID)."""

    def get_live_game_info(self, puuid: str) -> RawLiveGameData:
        """Return structured live game information for the player currently in-game.
        Includes all participants, champions, perks, spells, and roles."""

    def get_summoner_id(self, puuid: str) -> str:
        """Return encryptedSummonerId for given PUUID.
        Useful for endpoints requiring summoner-based identifiers."""

class StaticDataProviderInterface(ABC):
    def get_champion_data(self, champion_name: str) -> dict:
        """Fetch full champion data including spells, stats, and lore."""

    def get_all_champions(self) -> dict:
        """Return summary data for all champions (name, ID, tags)."""

    def get_spell_data(self) -> dict:
        """Return metadata for all summoner spells."""

    def get_item_data(self) -> dict:
        """Return metadata for all in-game items (cost, stats, effects)."""

    def get_rune_data(self) -> dict:
        """Return all runes trees and perk configurations."""

    def get_patch_version(self) -> str:
        """Return the latest game version string (e.g. '14.12.1') from Riot CDN."""
```

---

## 2️⃣ LLM Analysis Layer Interface

```python
from abc import ABC, abstractmethod
from core.models import matchup, threats

class LLMAnalyzerInterface(ABC):
    def analyze_lane(self, context: dict) -> matchup.LaneMatchupReport:
        """Analyze a lane matchup using an LLM.
        Expects context to include champions, runes, spells, and early stats."""

    def analyze_jungle(self, context: dict) -> matchup.JungleMatchupReport:
        """Analyze a jungle matchup, including 2v2 synergy with top laners."""

    def project_threats(self, context: dict) -> threats.ThreatProjectionResult:
        """Project late-game threats (1v1 and teamfights) based on team comps."""
```

---

## 3️⃣ Application Layer Interface

```python
from core.models import matchup, cooldowns, threats

class GameInsightAnalyzerInterface(ABC):
    def analyze_lane_matchup(self, user_champ: str, enemy_champ: str) -> matchup.LaneMatchupReport:
        """Analyze matchup between two champions on the same lane using LLM.
        Input: names of champions.
        Output: interpreted power spikes and style differences."""

    def analyze_jungle_matchup(self, ally_jg: str, enemy_jg: str) -> matchup.JungleMatchupReport:
        """Analyze the jungle duel + 2v2 potential between allied and enemy junglers."""

    def analyze_threats(self, full_game_data: dict) -> threats.ThreatProjectionResult:
        """Generate mid-to-late game threat projection from full team compositions."""

    def get_cooldown_table(self, champ1: str, champ2: str) -> cooldowns.CooldownTable:
        """Return per-level cooldown lists for both champions.
        Spells Q/W/E/R are expected, based on current skill order logic."""
```

---

## 4️⃣ Presentation Layer Interface

```python
from abc import ABC, abstractmethod
from pathlib import Path
from core.models.report import FullMatchReport

class ReportRendererInterface(ABC):
    def render_html_report(self, report_data: FullMatchReport, output_path: Path) -> None:
        """Render a styled HTML report file from a complete match analysis.
        The file will be written to the given output path."""

    def get_output_filename(self, summoner_name: str, timestamp: str) -> str:
        """Return a filename string using summoner name and timestamp.
        Format: 'report_{name}_{YYYY-MM-DD_HH-MM}.html'"""
```

## 🔧 Integration Layer Refinement

Following a detailed audit of Riot API and Data Dragon documentation, the following adjustments and clarifications apply to the Data Layer interfaces:

---

### ✅ RiotDataClientInterface (Updated)

```python
class RiotDataClientInterface(ABC):
    def get_puuid(self, game_name: str, tag_line: str) -> str:
        """Resolve Riot ID to account PUUID."""

    def get_live_game_info(self, puuid: str) -> RawLiveGameData:
        """Fetch current live game state for a player using their PUUID."""

    def get_summoner_id(self, puuid: str) -> str:
        """Resolve encryptedSummonerId from PUUID (needed for other endpoints)."""
```

📝 Note: Although the endpoint name is `/lol/spectator/v5/active-games/by-summoner/{}`, it correctly uses `puuid` — Riot’s naming inconsistency is acknowledged but behavior is correct.

---

### ✅ StaticDataProviderInterface (Expanded)

```python
class StaticDataProviderInterface(ABC):
    def get_champion_data(self, champion_name: str) -> dict:
        """Fetch full details for a single champion."""

    def get_all_champions(self) -> dict:
        """Fetch metadata for all champions (name, roles, IDs)."""

    def get_spell_data(self) -> dict: ...
    def get_item_data(self) -> dict: ...
    def get_rune_data(self) -> dict: ...
    def get_patch_version(self) -> str: ...
```

✅ `get_all_champions()` maps to:

```
GET /cdn/{VERSION}/data/{LANG}/champion.json
```

This may support champion selection logic or mapping IDs to names.

---

These refinements complete the interface-to-endpoint alignment and resolve naming mismatches or missing utility methods. All method signatures now match actual Riot/Dragon behavior.

## 📆 Folder and Module Naming Conventions

To ensure consistent, distributed implementation (especially with LLM-based actors), the following naming structure must be used:

### 📦 Core Models

- `core/models/`
  - Shared `pydantic` models for data transfer between all layers.
  - Recommended submodules:
    - `matchup.py` → LaneMatchupReport, JungleMatchupReport, StyleComparisonEntry, etc.
    - `cooldowns.py` → CooldownTable
    - `threats.py` → ThreatProjectionInput, ThreatProjectionResult
    - `report.py` → FullMatchReport
    - `raw_game_data.py` → RawLiveGameData, ParticipantInfo
    - `context.py` → LaneAnalysisContext, JungleAnalysisContext

### 🧱 System Layers

#### 1️⃣ Data Layer

- Folder: `data_providers/`
- Purpose: Access to Riot API and Data Dragon
- Modules:
  - `interfaces.py` → Abstract base interfaces (e.g., `RiotDataClientInterface`)
  - `riot_client.py` → Riot API implementation
  - `static_data.py` → Data Dragon implementation
  - `mock_data.py` *(optional)* → Mocks for offline testing

#### 2️⃣ LLM Analysis Layer

- Folder: `llm_analysis/`
- Purpose: Subjective evaluation using LLM agents
- Modules:
  - `interfaces.py` → `LLMAnalyzerInterface`
  - `gpt_lane_analyzer.py`, `gpt_jungle_analyzer.py`, etc. → Implementations

#### 3️⃣ Application Layer

- Folder: `application/` *(or alternatively `analyzers/`)*
- Purpose: Logic orchestration, coordination of lower layers
- Modules:
  - `interfaces.py` → `GameInsightAnalyzerInterface`
  - `game_analyzer.py` → High-level coordination logic

#### 4️⃣ Presentation Layer

- Folder: `presentation/`
- Purpose: Report rendering, HTML output
- Modules:
  - `interfaces.py` → `ReportRendererInterface`
  - `html_renderer.py` → Template-driven HTML report output

### 🧪 Test Structure (Recommended)

- `tests/` (mirrors above structure)
  - `test_data_providers/`
  - `test_llm_analysis/`
  - `test_application/`
  - `test_presentation/`

With this structure, all contributors—human or LLM—can easily locate their responsibilities, adhere to clean interfaces, and avoid conflicts or assumptions.