import pytest
from application.game_analyzer import GameInsightAnalyzer
from core.models import (
    GameData,
    LaneMatchupReport,
    JungleMatchupReport,
    ThreatProjectionReport,
    CooldownsComparisonReport,
    PlayerGameEntry,
    ChampionData,
    Runes,
    RuneEntry,
    TeamSide,
    PlayerRole,
    LaningDimension,
    JungleDimension
)

class DummyLLMAnalyzer:
    def start_context_window(self):
        pass

    def end_context_window(self):
        pass

    def get_lane_power_level(self, game_data, level):
        return ("Even", f"Level {level} comparison")

    def get_lane_extra_spikes(self, game_data):
        return {
            9: ("Stronger", "Power spike at 9"),
            11: ("Even", "Both spike at level 11"),
            13: ("Weaker", "Enemy powerspike at 13")
        }

    def get_lane_style_entry(self, game_data, dimension):
        return ("Moderate", "Moderate", f"Both are moderate in {dimension}")

    def get_jungle_dimension_entry(self, game_data, dimension):
        return ("Strong", "Weak", f"Ally strong in {dimension}, enemy weak")

    def get_teamfight_threats(self, game_data):
        return {"Aatrox": "Strong frontline", "Darius": "Moderate threat"}

    def get_sidelane_threats(self, game_data):
        return {"Aatrox": "Can 1v1 squishies", "Darius": "Good into tanks"}

    def get_cooldowns_leverage_suggestion(self, game_data):
        return "Exploit longer enemy W cooldown"


@pytest.fixture
def minimal_game_data():
    champ = ChampionData(
        name="Aatrox",
        base_hp=600,
        base_hp_regen=8,
        base_mp=0,
        base_mp_regen=0,
        base_armor=38,
        base_mr=32,
        base_ad=60,
        base_as=0.651,
        base_movespeed=345,
        base_range=175,
        hp_per_level=90,
        mp_per_level=0,
        armor_per_level=4.45,
        mr_per_level=2.05,
        ad_per_level=5,
        as_per_level=2.5,
        q_cooldowns=[14, 12, 10, 9, 7],
        w_cooldowns=[26, 23, 20, 17, 14],
        e_cooldowns=[9, 8, 7, 6, 5],
        r_cooldowns=[120, 100, 80]
    )
    runes = Runes(
        keystone=RuneEntry(name="Conqueror", shortDesc="Gain stacks on attacks"),
        primary=[],
        secondary=[],
        shards=[]
    )
    player = PlayerGameEntry(
        summoner_name="Cpt Szumi",
        champion=champ,
        runes=runes,
        summoner_spells=["Flash", "Ignite"],
        role="TOP",
        team="ALLY"
    )
    opponent = PlayerGameEntry(
        summoner_name="EnemyTop",
        champion=champ,
        runes=runes,
        summoner_spells=["Flash", "Teleport"],
        role="TOP",
        team="ENEMY"
    )
    return GameData(
        game_id="12345",
        summoner_name="Cpt Szumi",
        players=[player, opponent],
        user_role="TOP"
    )

def test_analyze_lane_matchup(minimal_game_data):
    analyzer = GameInsightAnalyzer(llm=DummyLLMAnalyzer())
    result = analyzer.analyze_lane_matchup(minimal_game_data)
    assert isinstance(result, LaneMatchupReport)
    assert result.level_1[0] in ["Weaker", "Even", "Stronger"]
    assert 9 in result.extra_spikes
    assert 11 in result.extra_spikes
    assert 13 in result.extra_spikes

def test_analyze_jungle_matchup(minimal_game_data):
    analyzer = GameInsightAnalyzer(llm=DummyLLMAnalyzer())
    result = analyzer.analyze_jungle_matchup(minimal_game_data)
    assert isinstance(result, JungleMatchupReport)
    assert isinstance(result.analysis, dict)
    for dimension in JungleDimension.__args__:
        assert dimension in result.analysis

def test_analyze_threats(minimal_game_data):
    analyzer = GameInsightAnalyzer(llm=DummyLLMAnalyzer())
    result = analyzer.analyze_threats(minimal_game_data)
    assert isinstance(result, ThreatProjectionReport)
    assert "Aatrox" in result.sidelane_threats
    assert "Darius" in result.teamfight_threats

def test_analyze_cooldowns(minimal_game_data):
    analyzer = GameInsightAnalyzer(llm=DummyLLMAnalyzer())
    result = analyzer.analyze_cooldowns(minimal_game_data)
    assert isinstance(result, CooldownsComparisonReport)
    assert isinstance(result.allyQ, dict)
    assert isinstance(result.enemyQ, dict)
    assert isinstance(result.cooldown_leverage_comment, str)
