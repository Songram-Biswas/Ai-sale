from __future__ import annotations

from typing import Any

import requests

from app.config import settings
from app.services.data_processor import DataProcessor
from app.utils.logger import get_logger


class DataCollectionAgent:
    def __init__(self, db: Any | None = None) -> None:
        self._db = db
        self._processor = DataProcessor()
        self._logger = get_logger(self.__class__.__name__, settings.log_level)

    def collect(self, company_url: str) -> dict:
        raw = self._fetch_company_data(company_url)
        processed = self._processor.process(raw)

        try:
            if self._db is not None:
                self._db["raw_events"].insert_one(
                    {"type": "company_scrape", "company_url": company_url, "raw": raw, "processed": processed}
                )
        except Exception:
            # intentionally minimal; DB may be unavailable in early scaffolding
            pass

        return {"company_url": company_url, "raw": raw, "processed": processed}

    def _fetch_company_data(self, company_url: str) -> dict:
        api_key = settings.firecrawl_api_key
        if not api_key:
            return self._mock_firecrawl(company_url, reason="missing FIRECRAWL_API_KEY")

        try:
            r = requests.post(
                "https://api.firecrawl.dev/v1/scrape",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"url": company_url, "formats": ["markdown"], "onlyMainContent": True},
                timeout=30,
            )
            r.raise_for_status()
            data = r.json()
            # Firecrawl commonly returns {success: bool, data: {...}}
            payload = data.get("data") if isinstance(data, dict) else None
            if not payload:
                return self._mock_firecrawl(company_url, reason="unexpected Firecrawl response shape")

            return {
                "source": "firecrawl",
                "url": company_url,
                "title": payload.get("metadata", {}).get("title"),
                "description": payload.get("metadata", {}).get("description"),
                "markdown": payload.get("markdown") or payload.get("content"),
                "metadata": payload.get("metadata", {}),
            }
        except Exception as e:
            self._logger.warning("firecrawl scrape failed: %s", str(e))
            return self._mock_firecrawl(company_url, reason="firecrawl request failed")

    @staticmethod
    def _mock_firecrawl(company_url: str, reason: str) -> dict:
        return {
            "source": "mock",
            "url": company_url,
            "title": None,
            "description": None,
            "markdown": f"(mock) Could not scrape. reason={reason}. url={company_url}",
            "metadata": {"reason": reason},
        }

