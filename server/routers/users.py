from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from dependencies.authentication import get_password_hash, get_current_active_user

from database.user_datalayer import UserDatalayer

from database.models.user import User as UserModel
from database.schemas.user import UserResponse, UserCreateRequest
from database.database import Base, SessionLocal, engine

from automapper import mapper

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


Base.metadata.create_all(bind=engine)


# Dependency
def get_db(request: Request):
    return request.state.db


# def map(user: UserModel) -> UserSchema:
#     return UserSchema(first_name=user.first_name, last_name=user.last_name, username=user.username
#                       , email=user.email, external_id=user.external_id)





@router.post("/users/", response_model=str, tags=["users"])
def create_user(user: UserCreateRequest, db: Session = Depends(get_db)):
    crud = UserDatalayer(db)
    db_user = crud.get_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = mapper.to(UserModel).map(user) 
    db_user = crud.create(user=db_user, hashed_password=get_password_hash(user.password))

    return str(db_user.external_id)


@router.get("/users", response_model=list[UserResponse], tags=["users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    crud = UserDatalayer(db)
    users = crud.get_users(skip, limit)
    return users


@router.get("/users/me", tags=["users"])
def read_user_me(current_user: Annotated[UserResponse, Depends(get_current_active_user)]):
    return current_user


@router.get("/users/email/{email}", response_model=UserResponse, tags=["users"])
def read_user_by_email(email: str, db: Session = Depends(get_db)):
    crud = UserDatalayer(db)
    db_user = crud.get_by_email(email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/ex_id/{external_user_id}", response_model=UserResponse, tags=["users"])
def read_user_by_external_id(external_user_id: UUID, db: Session = Depends(get_db)):
    crud = UserDatalayer(db)
    db_user = crud.get_by_external_id(external_user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# @router.get("/users/{user_id}", response_model=UserSchema, tags=["users"])
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     crud = UserDatalayer(db)
#     db_user = crud.get_by_id(user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
