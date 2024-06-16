from datetime import datetime, timedelta, timezone

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models.common.token import Token
from dependencies.authentication import create_access_token, authenticate_user, get_or_create_user
from sqlalchemy.orm import Session

from common.config import Settings
import httpx

settings = Settings()
router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

AUTH="auth"
INCORRECT_USERNAME_OR_PASSWORD = "Incorrect username or password"



# Dependency
def get_db(request: Request) -> Session:
    return request.state.db



async def get_github_access_token(request: Request, code: str, db: Session) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.github_url + "/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": settings.github_client_id,
                "client_secret": settings.github_client_secret,
                "code": code
            },
        )
        token_data = response.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            raise HTTPException(status_code=400, detail="OAuth token missing")
        
        user_response = await client.get(
            f"{settings.github_url}/api/v3/user", headers={"Authorization": f"Bearer {access_token}"}
        )
        user_data = user_response.json()
        
        username = user_data.get("login")
        email = user_data.get("email")
        user = get_or_create_user(db, username, email)

        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )

        return access_token
        



# @router.post("/users/", response_model=str, tags=[USERS])
# def create_user(user: UserCreateRequest, db: Session = Depends(get_db)):
#     crud = UserDatalayer(db)
#     user_dto = crud.get_by_email(email=user.email)
#     if user_dto:
#         raise HTTPException(status_code=400, detail=EMAIL_ALREADY_REGISTERED)
    
#     #user_dto = mapper.to(UserDto).map(user)
#     user_dto = UserDto(**user.model_dump(exclude_none='password'))
#     user_dto = crud.create(user=user_dto, hashed_password=get_password_hash(user.password))

#     return str(user_dto.external_id)



# https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/

@router.post("/auth/token", tags=[AUTH])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=INCORRECT_USERNAME_OR_PASSWORD,
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/auth/github", tags=[AUTH])
async def github_login():
    redirect_uri = f"{settings.host_url}/auth/github/callback"
    redirect_uri = "http://127.0.0.1:5500/login.html"
    return RedirectResponse(
        f"{settings.github_url}/login/oauth/authorize?client_id={settings.github_client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


@router.get("/auth/github/callback", tags=[AUTH])
async def github_callback(request: Request, code: str, db: Session = Depends(get_db)):
    access_token: str = await get_github_access_token(request, code, db)
    if settings.server_side_render:
        redirectResponse = RedirectResponse(url="/dashboard", status_code=303)
        redirectResponse.set_cookie(key="access_token", value=access_token, httponly=True)
        return redirectResponse
    
    # Client side
    return Token(access_token=access_token, token_type="bearer")

