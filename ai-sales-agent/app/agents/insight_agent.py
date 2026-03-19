# from __future__ import annotations

# import json
# from typing import Any

# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_openai import ChatOpenAI

# from app.config import settings
# from app.utils.logger import get_logger


# class InsightAgent:
#     def __init__(self, db: Any | None = None) -> None:
#         self._db = db
#         self._logger = get_logger(self.__class__.__name__, settings.log_level)

#     def generate_insights(self, company_profile: dict) -> dict:
#         """
#         Minimal deterministic insight generator.
#         Falls back to stub output if OPENAI_API_KEY isn't set.
#         """
#         if not settings.openai_api_key:
#             return self._stub(company_profile, reason="missing OPENAI_API_KEY")

#         llm = ChatOpenAI(
#             api_key=settings.openai_api_key,
#             model=settings.openai_model,
#             temperature=0,
#         )

#         system = SystemMessage(
#             content=(
#                 "You are a sales assistant. Output ONLY valid JSON. "
#                 "Be concise and deterministic. No markdown, no prose."
#             )
#         )
#         human = HumanMessage(
#             content=(
#                 "Given this company profile JSON, generate:\n"
#                 "- sales_insights: 3 bullets\n"
#                 "- pain_points: 3 bullets\n"
#                 "- hooks: 3 short outreach hooks\n"
#                 "Return as JSON with keys: sales_insights, pain_points, hooks.\n\n"
#                 f"company_profile={json.dumps(company_profile, ensure_ascii=False)}"
#             )
#         )

#         try:
#             resp = llm.invoke([system, human])
#             text = (resp.content or "").strip()
#             data = json.loads(text)
#             return {
#                 "sales_insights": data.get("sales_insights", []),
#                 "pain_points": data.get("pain_points", []),
#                 "hooks": data.get("hooks", []),
#                 "meta": {"model": settings.openai_model},
#             }
#         except Exception as e:
#             self._logger.warning("openai/langchain failed: %s", str(e))
#             return self._stub(company_profile, reason="openai/langchain invocation failed")

#     @staticmethod
#     def _stub(company_profile: dict, reason: str) -> dict:
#         name = (company_profile or {}).get("name") or "the company"
#         return {
#             "sales_insights": [f"(stub) {name} likely values faster pipeline.", "(stub) Prioritize ICP clarity.", "(stub) Focus on measurable ROI."],
#             "pain_points": ["(stub) Manual follow-ups.", "(stub) Low lead quality.", "(stub) Limited visibility into funnel."],
#             "hooks": [f"(stub) Quick idea to improve {name}'s outbound.", "(stub) 2-minute ROI calculator offer.", "(stub) Personalized teardown offer."],
#             "meta": {"reason": reason},
#         }

import openai
import json
import logging
from app.config import Config

logger = logging.getLogger(__name__)

class InsightAgent:
    def __init__(self):
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)

    def generate_insights(self, processed_data: dict):
        web_content = processed_data.get('cleaned_content', '')[:4000]
        company_url = processed_data.get('url', 'Unknown URL')
        
        prompt = f"""
        Analyze the company website content from {company_url} and provide a structured sales report.
        Content: {web_content}
        
        Return ONLY a valid JSON object with:
        1. "insights": A brief summary of what they do.
        2. "pain_points": A list of 3 potential challenges.
        3. "personalization_hooks": A list of 2 unique conversation starters.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a sales intelligence expert. Respond only in JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            return json.loads(response.choices[0].message.content)

        except Exception as e:
            logger.error(f"Error in OpenAI Agent: {str(e)}")
            return {
                "insights": "AI analysis failed due to quota or connection issues.",
                "pain_points": [f"Error: {str(e)[:50]}"],
                "personalization_hooks": []
            }