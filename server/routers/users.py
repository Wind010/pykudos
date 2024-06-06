from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from common.config import Settings
from dependencies.authentication import get_password_hash, get_current_active_user

from database.user_datalayer import UserDatalayer

from database.models.user import User as UserDto
from database.schemas.user import UserResponse, UserCreateRequest
from database.database import Base, engine
import httpx

#from automapper import mapper
settings = Settings()

router = APIRouter()
github_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


Base.metadata.create_all(bind=engine)

USERS = "users"
EMAIL_ALREADY_REGISTERED = "Email already registered"
USER_NOT_FOUND = "User not found"


# Dependencies
def get_db(request: Request) -> Session:
    return request.state.db


@router.post("/users/", response_model=str, tags=[USERS])
def create_user(user: UserCreateRequest, db: Session = Depends(get_db)):
    crud = UserDatalayer(db)
    user_dto = crud.get_by_email(email=user.email)
    if user_dto:
        raise HTTPException(status_code=400, detail=EMAIL_ALREADY_REGISTERED)
    
    #user_dto = mapper.to(UserDto).map(user)
    user_dto = UserDto(**user.model_dump(exclude_none='password'))
    user_dto = crud.create(user=user_dto, hashed_password=get_password_hash(user.password))

    return str(user_dto.external_id)


@router.get("/users", response_model=list[UserResponse], tags=[USERS])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    crud = UserDatalayer(db)
    users = crud.get_users(skip, limit)
    return users


@router.get("/users/github/team", tags=[USERS])
async  def read_users_github_team():
    url = f"{settings.github_url}/api/v3/orgs/{settings.github_orgs[0]}/teams/{settings.github_teams[0]}/members"
    headers = {'authorization': f"token {settings.github_pat}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status() 

    team_members = response.json()
    logins = [user["login"] for user in team_members if "login" in user]
    return {"logins": logins}


@router.get("/users/me", tags=[USERS])
def read_user_me(current_user: Annotated[UserResponse, Depends(get_current_active_user)]):
    return current_user


@router.get("/users/email/{email}", response_model=UserResponse, tags=[USERS])
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    crud = UserDatalayer(db)
    db_user = crud.get_by_email(email)
    if not db_user:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)
    return db_user


@router.get("/users/ex_id/{external_user_id}", response_model=UserResponse, tags=[USERS])
def read_user_by_external_id(external_user_id: UUID, db: Session = Depends(get_db)):
    crud = UserDatalayer(db)
    user_dto = crud.get_by_external_id(external_user_id)
    if not user_dto:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)
    return user_dto


# @router.get("/users/{user_id}", response_model=UserSchema, tags=[USERS])
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     crud = UserDatalayer(db)
#     db_user = crud.get_by_id(user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail=USER_NOT_FOUND)
#     return db_user
