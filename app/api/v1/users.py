from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.schemas.user import UserCreate, UserResponse
from fastapi import APIRouter
import app.core.models.users as models
from app.core.database import Base, engine
from app.api.deps import get_db
router = APIRouter()

@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.username == user.username),
                        )
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status = status.HTTP_400_BAD_REQUEST,
            detail = "Username already exists",
        )

    result = db.execute(select(models.User).where(models.User.email == user.email),
                        )
    existing_email = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status = status.HTTP_400_BAD_REQUEST,
            detail = "Email already exists",
        )
    
    new_user=  models.User(
        username = user.username,
        email = user.email,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post(
    "/users/{user_id}",
    response_model=UserResponse,
)
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalars().first()
    if user:
        return user
    else:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = "User not found")