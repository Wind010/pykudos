from pydantic import BaseModel
from datetime import datetime
from database.schemas.item import Item


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    username: str


class User(UserBase):
    """Domain object"""
    id: int
    is_active: bool
    is_admin: bool
    date_created: datetime
    date_modified: datetime
    items: list[Item] = []

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str