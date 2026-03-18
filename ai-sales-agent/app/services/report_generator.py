from __future__ import annotations

import json


class ReportGenerator:
    def generate_json(self, company: dict, insights: dict) -> dict:
        return {
            "company": company,
            "insights": {
                "sales_insights": insights.get("sales_insights", []),
                "pain_points": insights.get("pain_points", []),
                "hooks": insights.get("hooks", []),
            },
        }

    def generate_markdown(self, report_json: dict) -> str:
        company = report_json.get("company", {}) or {}
        insights = report_json.get("insights", {}) or {}

        def bullets(items):
            return "\n".join([f"- {x}" for x in (items or [])]) or "- (none)"

        md = []
        md.append(f"## Sales Report: {company.get('name') or 'Company'}")
        if company.get("url"):
            md.append(f"**URL:** {company['url']}")
        if company.get("description"):
            md.append(f"**Description:** {company['description']}")
        md.append("")
        md.append("### Sales insights")
        md.append(bullets(insights.get("sales_insights")))
        md.append("")
        md.append("### Pain points")
        md.append(bullets(insights.get("pain_points")))
        md.append("")
        md.append("### Hooks")
        md.append(bullets(insights.get("hooks")))
        return "\n".join(md).strip() + "\n"

    def generate(self, company: dict, insights: dict) -> dict:
        """
        Convenience wrapper that returns both formats.
        """
        report_json = self.generate_json(company=company, insights=insights)
        return {"json": report_json, "markdown": self.generate_markdown(report_json)}

    @staticmethod
    def dumps(report_json: dict) -> str:
        return json.dumps(report_json, ensure_ascii=False, indent=2)

