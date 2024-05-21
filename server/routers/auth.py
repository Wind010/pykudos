from datetime import datetime, timedelta, timezone

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models.common.token import Token
from dependencies.authentication import create_access_token, authenticate_user
from sqlalchemy.orm import Session

from common.config import Settings

settings = Settings()

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

INCORRECT_USERNAME_OR_PASSWORD = "Incorrect username or password"



# Dependency
def get_db(request: Request) -> Session:
    return request.state.db

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

@router.post("/auth/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if user is None:
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
