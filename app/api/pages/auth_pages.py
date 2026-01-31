from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import status

router = APIRouter()
templates = Jinja2Templates(directory=r"D:\Personal\code\rag_chatbot\app\templates")

@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request},
    )


@router.post("/login")
def login_submit(request: Request):
    """
    Handle login form submission.
    For now: placeholder.
    Later: validate credentials, set cookie / token, redirect.
    """
    # TODO: authenticate user
    return RedirectResponse(
        url="/",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.post("/logout")
def logout():
    """
    Clear auth state and redirect to home.
    """
    response = RedirectResponse(
        url="/",
        status_code=status.HTTP_303_SEE_OTHER,
    )
    # TODO: clear cookies / session
    return response
