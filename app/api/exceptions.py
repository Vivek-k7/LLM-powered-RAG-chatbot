from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory=r"D:\Personal\code\rag_chatbot\app\templates")

def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
):
    message = exc.detail or "An unexpected error occurred."

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": message},
        )

    # Page requests → HTML
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "status_code": exc.status_code,
            "title": f"Error {exc.status_code}",
            "message": message,
        },
        status_code=exc.status_code,
    )

def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    # API requests → JSON
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors()},
        )

    # Page requests → HTML
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "title": "Invalid Request",
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
