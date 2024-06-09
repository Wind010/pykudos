from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime


class ItemBase(BaseModel):
    #title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=600)
    is_oppertunity: bool = False


class Item(ItemBase):
    """Domain Object"""
    id: int
    user_id: int
    date_created: datetime
    date_modified: datetime

    class Config:
        orm_mode = True


class ItemCreateRequest(ItemBase):
    #external_user_id: UUID
    username: str



class ItemResponse(ItemBase):
    id: int
    date_created: datetime
    date_modified: datetime