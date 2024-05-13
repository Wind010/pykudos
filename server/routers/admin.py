from typing import Annotated
from fastapi import APIRouter, Depends
from functools import lru_cache

from common.config import Settings()
from dependencies.authentication import get_current_admin_user
from models.domain.users import DomainUser

router = APIRouter()

 
@lru_cache
def get_settings():
    return Settings()


@router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}


@router.get("/info")
async def info(current_user: Annotated[DomainUser, Depends(get_current_admin_user)]
               , settings: Annotated[Settings, Depends(get_settings)]):
    if current_user.is_admin:
        return { **settings.__dict__}