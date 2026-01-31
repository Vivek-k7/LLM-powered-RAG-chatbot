from fastapi import APIRouter
from app.api.v1 import health
from app.api.v1 import auth, users

router = APIRouter()

router.include_router(
    health.router,
    tags=["health"],
)

router.include_router(
    auth.router,
    tags=["auth"],
)

router.include_router(
    users.router,
    tags=["users"],
)
