from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from dependencies.authentication import get_password_hash, get_current_active_user

from database.user_datalayer import UserDatalayer

from database.models.user import User as UserModel
from database.schemas.user import User as UserSchema, UserCreate
from database.database import Base, SessionLocal, engine


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


Base.metadata.create_all(bind=engine)


# Dependency
def get_db(request: Request):
    return request.state.db


@router.post("/users/", response_model=UserSchema, tags=["users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    crud = UserDatalayer(db)
    db_user = crud.get_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create(user=user, hashed_password=get_password_hash(user.password))



@router.get("/users/", response_model=list[UserSchema], tags=["users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    crud = UserDatalayer(db)
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/me", tags=["users"])
def read_users_me(current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    return current_user


@router.get("/users/{email}", response_model=UserSchema, tags=["users"])
def read_user(email: str, db: Session = Depends(get_db)):
    crud = UserDatalayer(db)
    db_user = crud.get_by_email(email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/{user_id}", response_model=UserSchema, tags=["users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    crud = UserDatalayer(db)
    db_user = crud.get_by_id(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
