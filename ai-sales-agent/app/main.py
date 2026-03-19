# # from contextlib import asynccontextmanager

# # from fastapi import FastAPI

# # from app.api.routes import router
# # from app.config import settings
# # from app.models.db import mongodb
# # from app.utils.logger import get_logger

# # logger = get_logger("app", settings.log_level)


# # @asynccontextmanager
# # async def lifespan(app: FastAPI):
# #     logger.info("starting %s (%s)", settings.app_name, settings.environment)
# #     try:
# #         mongodb.connect()
# #     except Exception:
# #         logger.warning("mongodb connect failed (continuing)")
# #     yield
# #     try:
# #         mongodb.close()
# #     except Exception:
# #         logger.warning("mongodb close failed")
# #     logger.info("stopped")


# # app = FastAPI(title=settings.app_name, lifespan=lifespan)
# # app.include_router(router)

# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import traceback

# from app.agents.scraper import DataCollectionAgent
# from app.agents.processor import DataProcessor
# from app.agents.insight_agent import InsightAgent
# from app.database import Database
# from app.config import Config

# app = FastAPI(title="AI Sales Research Agent")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# try:
#     scraper = DataCollectionAgent()
#     processor = DataProcessor()
#     insight_gen = InsightAgent()
#     db = Database()
#     print(">>> Agents and Database initialized successfully.")
# except Exception as e:
#     print(f">>> Initialization Error: {e}")

# class AnalyzeRequest(BaseModel):
#     url: str

# @app.get("/")
# def home():
#     return {"status": "active", "message": "Server is running on port 8000"}

# @app.post("/analyze_company")
# async def analyze(request: AnalyzeRequest):
#     print(f"\n--- New Request: {request.url} ---")
    
#     try:
#         print("Step 1: Scraping started...")
#         raw_data = scraper.scrape(request.url)
#         if not raw_data or raw_data.get("title") == "Error":
#             raise ValueError(f"Scraping failed: {raw_data.get('content')}")
#         print("Step 1: Scraping complete.")
        
#         print("Step 2: Processing started...")
#         processed_data = processor.process(raw_data)
#         print("Step 2: Processing complete.")
        
#         print("Step 3: Generating AI Insights...")
#         insights = insight_gen.generate_insights(processed_data)
#         print("Step 4: AI Insights complete.")
        
#         result = {
#             "company_info": {
#                 "title": processed_data.get("title", "N/A"),
#                 "industry": processed_data.get("industry_guess", "General"),
#                 "description": processed_data.get("description", "")
#             },
#             "sales_intelligence": insights
#         }
        
#         try:
#             db.save_report(result)
#             if "_id" in result:
#                 del result["_id"]
#             print("Step 4: Report saved and cleaned.")
#         except Exception as db_err:
#             print(f"Step 4 Warning: DB save failed ({db_err})")
            
#         return result

#     except Exception as e:
#         print("!!! CRITICAL ERROR OCCURRED !!!")
#         print(traceback.format_exc()) 
#         raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.agents.scraper import DataCollectionAgent
from app.agents.processor import DataProcessor
from app.agents.insight_agent import InsightAgent
from app.database import Database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

scraper = DataCollectionAgent()
processor = DataProcessor()
insight_gen = InsightAgent()
db = Database()

class AnalyzeRequest(BaseModel):
    url: str

@app.post("/analyze_company")
async def analyze(request: AnalyzeRequest):
    try:
        raw_data = scraper.scrape(request.url)
        processed_data = processor.process(raw_data)
        insights = insight_gen.generate_insights(processed_data)
        
        result = {
            "company_info": {
                "title": processed_data.get("title"),
                "industry": processed_data.get("industry_guess"),
                "description": processed_data.get("description")
            },
            "sales_intelligence": insights
        }
        
        db.save_report(result)
        if "_id" in result:
            del result["_id"]
            
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))