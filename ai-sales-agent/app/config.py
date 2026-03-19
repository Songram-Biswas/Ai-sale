# from pydantic import Field
# from pydantic_settings import BaseSettings, SettingsConfigDict


# class Settings(BaseSettings):
#     model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

#     app_name: str = "ai-sales-agent"
#     environment: str = "development"
#     log_level: str = "INFO"

#     mongo_uri: str = Field(default="mongodb://localhost:27017", validation_alias="MONGO_URI")
#     mongo_db_name: str = Field(default="ai_sales_agent", validation_alias="MONGO_DB_NAME")

#     firecrawl_api_key: str | None = Field(default=None, validation_alias="FIRECRAWL_API_KEY")

#     openai_api_key: str | None = Field(default=None, validation_alias="OPENAI_API_KEY")
#     openai_model: str = Field(default="gpt-4o-mini", validation_alias="OPENAI_MODEL")


# settings = Settings()

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    MONGO_URI = os.getenv("MONGO_URI")
    FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")