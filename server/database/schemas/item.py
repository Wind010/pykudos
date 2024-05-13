from typing import Optional, Union
from pydantic import BaseModel
from datetime import datetime


class ItemBase(BaseModel):
    title: Optional[str]
    description: Optional[str] = None
    date_created: Optional[datetime]
    date_modified: Optional[datetime]


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class ItemCreate(ItemBase):
    pass

