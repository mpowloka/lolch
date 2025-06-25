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

### 🔹 PowerLevelEntry

```python
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

---

## 1️⃣ Data Layer Interface

```python
class RiotDataClientInterface(ABC):
    def get_puuid(self, game_name: str, tag_line: str) -> str: ...
    def get_live_game_info(self, puuid: str) -> RawLiveGameData: ...
    def get_summoner_id(self, puuid: str) -> str: ...
```

---

## 2️⃣ LLM Analysis Layer Interface

```python
class LLMAnalyzerInterface(ABC):
    def analyze_lane(self, context: dict) -> LaneMatchupReport: ...
    def analyze_jungle(self, context: dict) -> JungleMatchupReport: ...
    def project_threats(self, context: dict) -> ThreatProjectionResult: ...
```

---

## 3️⃣ Application Layer Interface

```python
class GameInsightAnalyzerInterface(ABC):
    def analyze_lane_matchup(self, user_champ: str, enemy_champ: str) -> LaneMatchupReport: ...
    def analyze_jungle_matchup(self, ally_jg: str, enemy_jg: str) -> JungleMatchupReport: ...
    def analyze_threats(self, full_game_data: dict) -> ThreatProjectionResult: ...
    def get_cooldown_table(self, champ1: str, champ2: str) -> CooldownTable: ...
```

---

## 4️⃣ Presentation Layer Interface

```python
class ReportRendererInterface(ABC):
    def render_html_report(self, report_data: FullMatchReport, output_path: Path) -> None: ...
    def get_output_filename(self, summoner_name: str, timestamp: str) -> str: ...
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
