import pytest
from llm_analysis.interfaces import LLMAnalyzerInterface
from llm_analysis.mock_analyzer import MockLLMAnalyzer
from core.models import (
    GameData,
    PlayerGameEntry,
    ChampionData,
    Runes,
    RuneEntry,
    LaningDimension,
    JungleDimension,
)

# Minimal dummy game data fixture
def create_dummy_game_data() -> GameData:
    champion = ChampionData(
        name="Aatrox",
        base_hp=600,
        base_hp_regen=8,
        base_mp=0,
        base_mp_regen=0,
        base_armor=38,
        base_mr=32,
        base_ad=60,
        base_as=0.7,
        base_movespeed=345,
        base_range=175,
        hp_per_level=90,
        mp_per_level=0,
        armor_per_level=4.5,
        mr_per_level=2.0,
        ad_per_level=5.0,
        as_per_level=2.5,
        q_cooldowns=[14, 12, 10, 9, 7],
        w_cooldowns=[26, 23, 20, 17, 14],
        e_cooldowns=[9, 8, 7, 6, 5],
        r_cooldowns=[120, 100, 80]
    )

    runes = Runes(
        keystone=RuneEntry(name="Conqueror", shortDesc="Stacking damage and healing"),
        primary=[],
        secondary=[],
        shards=[]
    )

    player = PlayerGameEntry(
        summoner_name="TestUser",
        champion=champion,
        runes=runes,
        summoner_spells=["Flash", "Ignite"],
        role="TOP",
        team="ALLY"
    )

    opponent = PlayerGameEntry(
        summoner_name="EnemyTop",
        champion=champion,
        runes=runes,
        summoner_spells=["Flash", "Teleport"],
        role="TOP",
        team="ENEMY"
    )

    return GameData(
        game_id="test123",
        summoner_name="TestUser",
        players=[player, opponent],
        user_role="TOP"
    )

@pytest.fixture
def analyzer() -> LLMAnalyzerInterface:
    return MockLLMAnalyzer()

@pytest.fixture
def game_data() -> GameData:
    return create_dummy_game_data()

def test_lane_power_levels(analyzer, game_data):
    for level in range(1, 7):
        comp, reason = analyzer.get_lane_power_level(game_data, level)
        assert comp in ("Weaker", "Even", "Stronger")
        assert isinstance(reason, str)

def test_lane_style_dimensions(analyzer, game_data):
    for dimension in LaningDimension.__args__:
        ally, enemy, comment = analyzer.get_lane_style_entry(game_data, dimension)
        assert ally in ("Very Weak", "Weak", "Moderate", "Strong", "Very Strong")
        assert enemy in ("Very Weak", "Weak", "Moderate", "Strong", "Very Strong")
        assert isinstance(comment, str)

def test_jungle_dimensions(analyzer, game_data):
    for dimension in JungleDimension.__args__:
        ally, enemy, comment = analyzer.get_jungle_dimension_entry(game_data, dimension)
        assert ally in ("Very Weak", "Weak", "Moderate", "Strong", "Very Strong")
        assert enemy in ("Very Weak", "Weak", "Moderate", "Strong", "Very Strong")
        assert isinstance(comment, str)

def test_extra_spikes(analyzer, game_data):
    spikes = analyzer.get_lane_extra_spikes(game_data)
    for level, (comp, comment) in spikes.items():
        assert isinstance(level, int)
        assert comp in ("Weaker", "Even", "Stronger")
        assert isinstance(comment, str)

def test_threat_outputs(analyzer, game_data):
    teamfight = analyzer.get_teamfight_threats(game_data)
    sidelane = analyzer.get_sidelane_threats(game_data)
    assert isinstance(teamfight, dict)
    assert isinstance(sidelane, dict)
    for name, desc in teamfight.items():
        assert isinstance(name, str)
        assert isinstance(desc, str)
    for name, desc in sidelane.items():
        assert isinstance(name, str)
        assert isinstance(desc, str)

def test_cooldown_suggestion(analyzer, game_data):
    result = analyzer.get_cooldowns_leverage_suggestion(game_data)
    assert isinstance(result, str)

def test_context_lifecycle(analyzer):
    analyzer.start_context_window()
    analyzer.end_context_window()
