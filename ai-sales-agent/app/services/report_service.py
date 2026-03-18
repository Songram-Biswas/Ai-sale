from __future__ import annotations

from typing import Any


class ReportService:
    def __init__(self, reports_collection: Any) -> None:
        self._reports = reports_collection

    def generate(self, company_id: str | None, inputs: dict) -> dict:
        # placeholder: minimal report payload
        report = {
            "company_id": company_id,
            "report": {"title": "Generated Report (stub)", "inputs": inputs},
        }
        try:
            result = self._reports.insert_one(report)
            report_id = str(result.inserted_id)
        except Exception:
            report_id = None

        return {"report_id": report_id, "report": report["report"]}

