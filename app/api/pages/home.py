from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.core.models.users import User
from app.schemas.user import UserCreate, UserResponse
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.models.users import User
templates = Jinja2Templates(directory=r"D:\Personal\code\rag_chatbot\app\templates")

router = APIRouter()

@router.get("/home")
def home(request: Request):
    current_user = None
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "user": current_user,  # ORM User instance
        },
    )
