import datetime
from pathlib import Path

from data_providers.riot_client import RiotAPIClient
from data_providers.static_data import DataDragonClient
from application.game_analyzer import GameInsightAnalyzer
from presentation.html_renderer import HTMLReportRenderer
from llm_analysis.mock_analyzer import MockLLMAnalyzer

# Credentials and summoner info from `my user data.txt`
RIOT_TOKEN = "RGAPI-e2126839-d146-4b52-a98d-13e483c1baca"
GAME_NAME = "Cpt Szumi"
TAG_LINE = "EUNE"
REGION = "europe"
SERVER = "euw1"

# Main orchestrator
class InsightRunner:
    def __init__(self):
        self.riot_client = RiotAPIClient(RIOT_TOKEN, REGION, SERVER)
        self.static_provider = DataDragonClient()
        self.analyzer = GameInsightAnalyzer(self.riot_client, self.static_provider, MockLLMAnalyzer())
        self.renderer = HTMLReportRenderer()

    def _generate_filename(self, summoner_name: str) -> Path:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = self.renderer.get_output_filename(summoner_name, timestamp)
        return Path("reports") / filename

    def run_live_game(self):
        puuid = self.riot_client.get_puuid(GAME_NAME, TAG_LINE)
        live_game = self.riot_client.get_live_game_info(puuid)
        if not live_game:
            print("🔁 Not currently in a live game.")
            return

        report = self.analyzer.generate_full_report_from_live(live_game)
        output_path = self._generate_filename(report.summoner_name)
        self.renderer.render_html_report(report, output_path)
        print(f"✅ Live game report saved to {output_path}")

    def run_last_game(self):
        puuid = self.riot_client.get_puuid(GAME_NAME, TAG_LINE)
        match_ids = self.riot_client.get_recent_match_ids(puuid, count=1)
        if not match_ids:
            print("⚠️ No recent matches found.")
            return

        match_data = self.riot_client.get_match_data(match_ids[0])
        summary = self.riot_client.extract_match_participant_summary(match_data, puuid)

        lane = self.analyzer.analyze_lane_matchup(summary["user_champion"], summary["enemy_champion"])
        jungle = self.analyzer.analyze_jungle_matchup(summary["ally_jungler"], summary["enemy_jungler"])
        cooldowns = self.analyzer.get_cooldown_table(summary["user_champion"], summary["enemy_champion"])
        threats = self.analyzer.analyze_threats({
            "blue_team": summary["blue_team"],
            "red_team": summary["red_team"],
            "roles": summary["roles"]
        })

        from core.models import FullMatchReport
        report = FullMatchReport(
            summoner_name=summary["summoner_name"],
            lane=lane,
            jungle=jungle,
            cooldowns=cooldowns,
            threats=threats
        )
        output_path = self._generate_filename(report.summoner_name)
        self.renderer.render_html_report(report, output_path)
        print(f"✅ Last game report saved to {output_path}")


# ---- Entry Point ----
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run full game insight analysis.")
    parser.add_argument("mode", choices=["live", "last"], help="Game mode to analyze")
    args = parser.parse_args()

    runner = InsightRunner()
    if args.mode == "live":
        runner.run_live_game()
    else:
        runner.run_last_game()
