from fastapi import FastAPI,status
from fastapi.exceptions import RequestValidationError
from app.api.exceptions import validation_exception_handler, http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.schemas.user import UserCreate, UserResponse
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.lifespan import lifespan
from app.api.v1.router import router as api_v1_router
from app.api.pages.home import router as home_router
from app.api.pages.auth_pages import router as auth_router

setup_logging()

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/media", StaticFiles(directory="app/media"), name="media")

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.include_router(home_router)
app.include_router(auth_router)
app.include_router(api_v1_router, prefix="/api/v1")


