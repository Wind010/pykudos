from typing import Annotated
from fastapi import FastAPI, Form
from fastapi import APIRouter, Depends, HTTPException, Request, status

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from common.config import Settings
from database.models.user import User
from dependencies.authentication import get_current_active_user
from sqlalchemy.orm import Session
from models.common.token import TokenData


settings = Settings()
router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_db(request: Request):
    return request.state.db


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request,  "enable_local_auth": settings.enable_local_auth
                                                     , "enable_github_auth": settings.enable_github_auth})
    
@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request, user: TokenData = Depends(get_current_active_user)):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# @router.get("/", response_class=HTMLResponse)
# async def home_page(request: Request, user: TokenData = Depends(get_current_active_user)):
#     return templates.TemplateResponse("home.html", {"request": request})