from __future__ import annotations

import json
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.config import settings
from app.utils.logger import get_logger


class InsightAgent:
    def __init__(self, db: Any | None = None) -> None:
        self._db = db
        self._logger = get_logger(self.__class__.__name__, settings.log_level)

    def generate_insights(self, company_profile: dict) -> dict:
        """
        Minimal deterministic insight generator.
        Falls back to stub output if OPENAI_API_KEY isn't set.
        """
        if not settings.openai_api_key:
            return self._stub(company_profile, reason="missing OPENAI_API_KEY")

        llm = ChatOpenAI(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            temperature=0,
        )

        system = SystemMessage(
            content=(
                "You are a sales assistant. Output ONLY valid JSON. "
                "Be concise and deterministic. No markdown, no prose."
            )
        )
        human = HumanMessage(
            content=(
                "Given this company profile JSON, generate:\n"
                "- sales_insights: 3 bullets\n"
                "- pain_points: 3 bullets\n"
                "- hooks: 3 short outreach hooks\n"
                "Return as JSON with keys: sales_insights, pain_points, hooks.\n\n"
                f"company_profile={json.dumps(company_profile, ensure_ascii=False)}"
            )
        )

        try:
            resp = llm.invoke([system, human])
            text = (resp.content or "").strip()
            data = json.loads(text)
            return {
                "sales_insights": data.get("sales_insights", []),
                "pain_points": data.get("pain_points", []),
                "hooks": data.get("hooks", []),
                "meta": {"model": settings.openai_model},
            }
        except Exception as e:
            self._logger.warning("openai/langchain failed: %s", str(e))
            return self._stub(company_profile, reason="openai/langchain invocation failed")

    @staticmethod
    def _stub(company_profile: dict, reason: str) -> dict:
        name = (company_profile or {}).get("name") or "the company"
        return {
            "sales_insights": [f"(stub) {name} likely values faster pipeline.", "(stub) Prioritize ICP clarity.", "(stub) Focus on measurable ROI."],
            "pain_points": ["(stub) Manual follow-ups.", "(stub) Low lead quality.", "(stub) Limited visibility into funnel."],
            "hooks": [f"(stub) Quick idea to improve {name}'s outbound.", "(stub) 2-minute ROI calculator offer.", "(stub) Personalized teardown offer."],
            "meta": {"reason": reason},
        }

