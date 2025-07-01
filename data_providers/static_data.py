# static_data.py
from data_providers.interfaces import StaticDataProviderInterface
from data_providers._internal.config import get_headers, get_cdn_url
from data_providers._internal.http_client import HttpClient
from data_providers._internal.cache import CDNCache
from data_providers._internal.version_tracker import VersionTracker
from data_providers._internal.errors import StaticDataNotFound
from core.models import ChampionData, RuneEntry, SummonerSpell

class StaticDataProvider(StaticDataProviderInterface):
    def __init__(self, lang="en_US"):
        self.lang = lang
        self.http = HttpClient()
        self.cache = CDNCache()
        self.version_tracker = VersionTracker()
        self._version = None

    def get_patch_version(self) -> str:
        if self._version:
            return self._version
        url = "https://ddragon.leagueoflegends.com/api/versions.json"
        versions = self.http.get(url)
        self._version = versions[0]
        return self._version

    def _ensure_cache_valid(self):
        version = self.get_patch_version()
        if self.version_tracker.has_changed(version):
            self.cache.invalidate_all()
            self.version_tracker.set_version(version)

    def get_all_champions(self) -> dict[str, ChampionData]:
        self._ensure_cache_valid()
        cache_key = "champion_list"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        url = get_cdn_url(self._version, self.lang, "champion.json")
        raw = self.http.get(url)
        parsed = {}
        for champ in raw["data"].values():
            parsed[champ["id"]] = ChampionData(
                name=champ["id"],
                base_hp=champ["stats"]["hp"],
                base_hp_regen=champ["stats"]["hpregen"],
                base_mp=champ["stats"]["mp"],
                base_mp_regen=champ["stats"]["mpregen"],
                base_armor=champ["stats"]["armor"],
                base_mr=champ["stats"]["spellblock"],
                base_ad=champ["stats"]["attackdamage"],
                base_as=champ["stats"]["attackspeed"],
                base_movespeed=champ["stats"]["movespeed"],
                base_range=champ["stats"]["attackrange"],
                hp_per_level=champ["stats"]["hpperlevel"],
                mp_per_level=champ["stats"]["mpperlevel"],
                armor_per_level=champ["stats"]["armorperlevel"],
                mr_per_level=champ["stats"]["spellblockperlevel"],
                ad_per_level=champ["stats"]["attackdamageperlevel"],
                as_per_level=champ["stats"]["attackspeedperlevel"],
                q_cooldowns=[],
                w_cooldowns=[],
                e_cooldowns=[],
                r_cooldowns=[],
            )
        self.cache.set(cache_key, parsed)
        return parsed

    def get_champion_data(self, champion_name: str) -> ChampionData:
        self._ensure_cache_valid()
        cache_key = f"champion_detail_{champion_name}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        url = get_cdn_url(self._version, self.lang, f"champion/{champion_name}.json")
        raw = self.http.get(url)
        data = raw["data"][champion_name]
        stats = data["stats"]
        spells = data["spells"]

        champ = ChampionData(
            name=champion_name,
            base_hp=stats["hp"],
            base_hp_regen=stats["hpregen"],
            base_mp=stats["mp"],
            base_mp_regen=stats["mpregen"],
            base_armor=stats["armor"],
            base_mr=stats["spellblock"],
            base_ad=stats["attackdamage"],
            base_as=stats["attackspeed"],
            base_movespeed=stats["movespeed"],
            base_range=stats["attackrange"],
            hp_per_level=stats["hpperlevel"],
            mp_per_level=stats["mpperlevel"],
            armor_per_level=stats["armorperlevel"],
            mr_per_level=stats["spellblockperlevel"],
            ad_per_level=stats["attackdamageperlevel"],
            as_per_level=stats["attackspeedperlevel"],
            q_cooldowns=spells[0]["cooldown"],
            w_cooldowns=spells[1]["cooldown"],
            e_cooldowns=spells[2]["cooldown"],
            r_cooldowns=spells[3]["cooldown"],
        )
        self.cache.set(cache_key, champ)
        return champ

    def get_all_runes(self) -> dict[str, RuneEntry]:
        self._ensure_cache_valid()
        cache_key = "runes"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        url = get_cdn_url(self._version, self.lang, "runesReforged.json")
        raw = self.http.get(url)
        parsed = {}
        for tree in raw:
            for slot in tree.get("slots", []):
                for rune in slot.get("runes", []):
                    parsed[rune["name"]] = RuneEntry(
                        name=rune["name"],
                        shortDesc=rune.get("shortDesc", "")
                    )
        self.cache.set(cache_key, parsed)
        return parsed

    def get_spell_data(self) -> dict[str, SummonerSpell]:
        self._ensure_cache_valid()
        cache_key = "spells"
        cached = self.cache.get(cache_key)
        if cached:
            return cached
        url = get_cdn_url(self._version, self.lang, "summoner.json")
        raw = self.http.get(url)
        parsed = {}
        for spell in raw["data"].values():
            parsed[spell["name"]] = SummonerSpell(
                name=spell["name"],
                cooldown=[float(cd) for cd in ([spell["cooldown"]] if isinstance(spell["cooldown"], (int, float)) else spell["cooldown"])],
                description=spell.get("description", "")
            )
        self.cache.set(cache_key, parsed)
        return parsed
