from __future__ import annotations

from typing import Any


class CompanyAnalyzer:
    def __init__(self, companies_collection: Any) -> None:
        self._companies = companies_collection

    def analyze(self, company: dict) -> dict:
        # placeholder: store input and return a minimal "analysis"
        doc = {"company": company, "analysis": {"status": "stub"}}
        try:
            result = self._companies.insert_one(doc)
            company_id = str(result.inserted_id)
        except Exception:
            company_id = None

        return {"company_id": company_id, "analysis": doc["analysis"]}

