from core.models import GameData, PlayerGameEntry, PlayerRole, TeamSide, Runes, RuneEntry
from core.models import SummonerSpell, ChampionData
from data_providers.static_data import StaticDataProvider

def map_raw_to_game_data(raw_data: dict, user_name: str, static: StaticDataProvider) -> GameData:
    runes_lookup = static.get_all_runes()
    spells_lookup = static.get_spell_data()
    players = []

    for p in raw_data.get("participants", []):
        role = p.get("teamPosition", "TOP")
        team = "ALLY" if p.get("summonerName", "") == user_name else "ENEMY"
        champ = static.get_champion_data(p.get("championName", "Aatrox"))

        primary = []
        secondary = []
        shards = []
        for s in p.get("perks", {}).get("styles", []):
            if s.get("description") == "primaryStyle":
                primary = [runes_lookup.get(r.get("name"), None) for r in s.get("selections", []) if runes_lookup.get(r.get("name"))]
            elif s.get("description") == "subStyle":
                secondary = [runes_lookup.get(r.get("name"), None) for r in s.get("selections", []) if runes_lookup.get(r.get("name"))]
        shards = [runes_lookup.get(str(s), RuneEntry(name=f"Shard {s}", shortDesc="")) for s in p.get("perks", {}).get("statPerks", {}).values()]

        runes = Runes(
            keystone=primary[0] if primary else RuneEntry(name="Unknown", shortDesc=""),
            primary=primary,
            secondary=secondary,
            shards=shards,
        )

        spell_names = [p.get("summoner1Id"), p.get("summoner2Id")]
        spell_list = []
        for sid in spell_names:
            for name, spell in spells_lookup.items():
                if str(sid) in name or name.lower().startswith("summoner"):
                    spell_list.append(name)
                    break

        full_champ_data = static.get_champion_data(p.get("championName", "Aatrox"))

        entry = PlayerGameEntry(
            summoner_name=p.get("summonerName", ""),
            champion=full_champ_data,
            runes=runes,
            summoner_spells=spell_list,
            role=role,
            team=team,
        )
        players.append(entry)

    user_role = next((p.role for p in players if p.summoner_name == user_name), "TOP")

    return GameData(
        game_id=str(raw_data.get("gameId", "unknown")),
        summoner_name=user_name,
        players=players,
        user_role=user_role,
    )
