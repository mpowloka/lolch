import os
import pytest
from data_providers.riot_client import RiotApiClient
from data_providers.static_data import StaticDataProvider
from data_providers.game_data_assembler import GameDataAssembler
from core.models import GameData, ChampionData, RuneEntry, SummonerSpell

TEST_GAME_NAME = os.environ.get("TEST_GAME_NAME", "Cpt Szumi")
TEST_TAG_LINE = os.environ.get("TEST_TAG_LINE", "EUNE")

@pytest.fixture(scope="module")
def riot_client():
    return RiotApiClient()

@pytest.fixture(scope="module")
def static_provider():
    return StaticDataProvider()

@pytest.fixture(scope="module")
def data_assembler():
    return GameDataAssembler()

def test_get_puuid(riot_client):
    puuid = riot_client.get_puuid(TEST_GAME_NAME, TEST_TAG_LINE)
    assert isinstance(puuid, str)
    assert len(puuid) > 10

def test_get_patch_version(static_provider):
    version = static_provider.get_patch_version()
    assert isinstance(version, str)
    assert version.count(".") >= 1

def test_get_all_champions(static_provider):
    champions = static_provider.get_all_champions()
    assert isinstance(champions, dict)
    sample = next(iter(champions.values()))
    assert isinstance(sample, ChampionData)

def test_get_champion_data_and_cooldowns(static_provider):
    champ = static_provider.get_champion_data("Aatrox")
    assert isinstance(champ, ChampionData)
    assert champ.q_cooldowns and isinstance(champ.q_cooldowns[0], (int, float))

def test_get_all_runes(static_provider):
    runes = static_provider.get_all_runes()
    assert isinstance(runes, dict)
    sample = next(iter(runes.values()))
    assert isinstance(sample, RuneEntry)

def test_get_spell_data(static_provider):
    spells = static_provider.get_spell_data()
    assert isinstance(spells, dict)
    sample = next(iter(spells.values()))
    assert isinstance(sample, SummonerSpell)

def test_recent_match_ids(riot_client):
    puuid = riot_client.get_puuid(TEST_GAME_NAME, TEST_TAG_LINE)
    match_ids = riot_client.get_match_ids(puuid, count=5)
    assert isinstance(match_ids, list)
    assert len(match_ids) > 0
    assert all(isinstance(mid, str) for mid in match_ids)

def test_get_match_details(riot_client):
    puuid = riot_client.get_puuid(TEST_GAME_NAME, TEST_TAG_LINE)
    match_ids = riot_client.get_match_ids(puuid, count=1)
    details = riot_client.get_match_details(match_ids[0])
    assert isinstance(details, dict)
    assert 'metadata' in details

def test_game_data_from_live_game(data_assembler):
    try:
        game_data = data_assembler.get_live_game_info(TEST_GAME_NAME, TEST_TAG_LINE)
        assert isinstance(game_data, GameData)
        assert game_data.summoner_name == TEST_GAME_NAME
    except Exception as e:
        if "not in a game" in str(e).lower():
            pytest.skip("User not currently in a live match")
        else:
            raise

def test_game_data_from_match(data_assembler, riot_client):
    puuid = riot_client.get_puuid(TEST_GAME_NAME, TEST_TAG_LINE)
    match_ids = riot_client.get_match_ids(puuid, count=1)
    game_data = data_assembler.get_historical_game(match_ids[0], TEST_GAME_NAME, TEST_TAG_LINE)
    assert isinstance(game_data, GameData)
    assert game_data.summoner_name == TEST_GAME_NAME

def test_recent_game_ids(data_assembler):
    ids = data_assembler.get_recent_game_ids(TEST_GAME_NAME, TEST_TAG_LINE)
    assert isinstance(ids, list)
    assert all(isinstance(i, str) for i in ids)
    assert len(ids) > 0
