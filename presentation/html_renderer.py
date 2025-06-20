from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from core.models.report import FullMatchReport

class HTMLReportRenderer:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader(str("presentation/templates")))
        self.template = self.env.get_template("jinja_report_template_v0.1.0.html")

    def render_html_report(self, report_data: FullMatchReport, output_path: Path) -> None:
        context = self._prepare_context(report_data)
        html = self.template.render(**context)
        output_path.write_text(html, encoding='utf-8')

    def get_output_filename(self, summoner_name: str, timestamp: str) -> str:
        return f"report_{summoner_name}_{timestamp}.html"

    def _prepare_context(self, report: FullMatchReport) -> dict:
        def icon(status: str) -> str:
            return {
                "Stronger": "⬆️ Stronger",
                "Weaker": "⬇️ Weaker",
                "Even": "⚖️ Even"
            }.get(status, "?")

        return {
            "summoner_name": report.summoner_name,
            "lane": report.lane,
            "jungle": report.jungle,
            "cooldowns": report.cooldowns,
            "threats": report.threats,
            "icon_for_status": icon  # Pass helper to Jinja
        }
