from contextlib import asynccontextmanager
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app):
    logger.info("Application startup")
    yield
    logger.info("Application shutdown")
