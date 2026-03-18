from fastapi import APIRouter
from pydantic import BaseModel, HttpUrl

from app.models.db import mongodb
from app.agents.data_collection_agent import DataCollectionAgent
from app.agents.insight_agent import InsightAgent
from app.services.report_generator import ReportGenerator

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


class AnalyzeCompanyRequest(BaseModel):
    company_url: HttpUrl


@router.post("/analyze_company")
def analyze_company(body: AnalyzeCompanyRequest):
    company_url = str(body.company_url)

    collector = DataCollectionAgent(db=mongodb.db)
    collected = collector.collect(company_url)
    normalized = collected.get("processed", {}).get("normalized") or {}

    company_profile = {
        "url": normalized.get("url") or company_url,
        "name": normalized.get("name"),
        "description": normalized.get("description"),
        "content_markdown": normalized.get("content_markdown"),
    }

    insights = InsightAgent(db=mongodb.db).generate_insights(company_profile)

    # Store minimal documents (ignore failures for early-stage usability)
    company_id = None
    try:
        r = mongodb.companies.insert_one({"company_url": company_url, "profile": company_profile})
        company_id = str(r.inserted_id)
    except Exception:
        pass

    try:
        mongodb.reports.insert_one({"company_id": company_id, "company_url": company_url, "insights": insights})
    except Exception:
        pass

    return {"company_id": company_id, "company": company_profile, "insights": insights}


class GenerateReportRequest(BaseModel):
    company: dict = {}
    insights: dict = {}
    format: str = "both"  # both|json|markdown


@router.post("/generate_report")
def generate_report(body: GenerateReportRequest):
    gen = ReportGenerator()
    out = gen.generate(company=body.company, insights=body.insights)

    fmt = (body.format or "both").lower()
    if fmt == "json":
        return {"json": out["json"]}
    if fmt == "markdown":
        return {"markdown": out["markdown"]}
    return out

