from pathlib import Path
from core.models.matchup import (
    PowerLevelEntry,
    StyleComparisonEntry,
    LaneMatchupReport,
    JungleMatchupReport,
    JungleMatchupEntry,
)
from core.models.cooldowns import CooldownTable
from core.models.threats import ThreatProjectionResult
from core.models.report import FullMatchReport
from presentation.renderer import HTMLReportRenderer

if __name__ == "__main__":
    report = FullMatchReport(
        summoner_name="Cpt Szumi",
        lane=LaneMatchupReport(
            champion_1="Teemo",
            champion_2="Garen",
            power_levels=[
                PowerLevelEntry(level=1, status="Weaker", comment="Garen has silence and burst"),
                PowerLevelEntry(level=3, status="Stronger", comment="Teemo can kite with Q and poison"),
                PowerLevelEntry(level=6, status="Stronger", comment="Mushroom traps give strong control")
            ],
            style_comparison=[
                StyleComparisonEntry(dimension="Sustain", ally="Low", enemy="High"),
                StyleComparisonEntry(dimension="Waveclear", ally="Medium", enemy="High"),
                StyleComparisonEntry(dimension="Trading", ally="Poke", enemy="Burst"),
                StyleComparisonEntry(dimension="Mana/Energy", ally="None", enemy="None"),
                StyleComparisonEntry(dimension="Roaming", ally="Low", enemy="Medium")
            ],
            tips=["Stay out of brush early", "Use blind on Garen's Q timing"]
        ),
        jungle=JungleMatchupReport(
            champion_1="Nunu",
            champion_2="Warwick",
            entries=[
                JungleMatchupEntry(dimension="Clear Speed", ally="Fast", enemy="Average"),
                JungleMatchupEntry(dimension="Gank Threat", ally="High", enemy="High"),
                JungleMatchupEntry(dimension="1v1", ally="Even", enemy="Even"),
                JungleMatchupEntry(dimension="2v2 Synergy", ally="Teemo poke + Nunu CC", enemy="Garen burst + Warwick sustain")
            ]
        ),
        cooldowns=CooldownTable(spells={
            "Q": {"champion_1": [8, 7, 6], "champion_2": [8, 7, 6]},
            "W": {"champion_1": [14, 12, 10], "champion_2": [15, 13, 11]},
            "E": {"champion_1": [10, 9, 8], "champion_2": [9, 8, 7]},
            "R": {"champion_1": [90, 75, 60], "champion_2": [120, 100, 80]}
        }),
        threats=ThreatProjectionResult(
            sidelane_threats=["Yasuo", "Irelia"],
            teamfight_threats=["Miss Fortune", "Amumu"]
        )
    )

    template_dir = Path("presentation/templates")
    output_path = Path("report_Teemo_vs_Garen.html")
    renderer = HTMLReportRenderer(template_dir)
    renderer.render_html_report(report, output_path)
    print(f"✅ Report generated: {output_path}")
