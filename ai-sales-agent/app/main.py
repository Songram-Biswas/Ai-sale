from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.config import settings
from app.models.db import mongodb
from app.utils.logger import get_logger

logger = get_logger("app", settings.log_level)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("starting %s (%s)", settings.app_name, settings.environment)
    try:
        mongodb.connect()
    except Exception:
        logger.warning("mongodb connect failed (continuing)")
    yield
    try:
        mongodb.close()
    except Exception:
        logger.warning("mongodb close failed")
    logger.info("stopped")


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(router)

