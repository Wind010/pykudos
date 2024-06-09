from typing import Annotated
from uuid import UUID
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from database.database import SessionLocal, engine

from database.models.item import Item as ItemDto
from database.schemas.item import ItemResponse, ItemCreateRequest

from database.item_datalayer import ItemDatalayer
from database.user_datalayer import UserDatalayer
from dependencies.authentication import get_current_active_user
from models.common.token import TokenData


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


ITEM = "item"
ITEM_NOT_FOUND = "Item not found."


# Dependency
def get_db(request: Request):
    return request.state.db


@router.post(f"/{ITEM}/", response_model=int, tags=[ITEM])
def create_item(item: ItemCreateRequest, db: Session = Depends(get_db)
                , token: TokenData = Depends(get_current_active_user)):
    user_db, item_db = UserDatalayer(db), ItemDatalayer(db)
    
    #user_dto = user_db.get_by_external_id(item.external_user_id)
    source_user = user_db.get_by_username(token.username)
    target_user = user_db.get_by_username(item.username)
    
    if not source_user:
        raise HTTPException(status_code=400, detail="Source user not found")
    
    if not target_user:
        raise HTTPException(status_code=400, detail="Target user not found")
    
    item_dto = ItemDto(**item.model_dump(exclude={'external_user_id', 'username'})
                       , source_user_id=source_user.id, target_user_id=target_user.id)
    item_dto.source_user_id = source_user.id
    item_dto.target_user_id = target_user.id

    item_dto = item_db.create(item=item_dto)

    return item_dto.id


@router.get("/items/{external_user_id}", response_model=list[ItemResponse], tags=[ITEM])
async def read_items(external_user_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
                    , token: TokenData = Depends(get_current_active_user)):
    #TODO:  Validate token
    user_db, item_db = UserDatalayer(db), ItemDatalayer(db)

    #user_dto = user_db.get_by_external_id(item.external_user_id)
    user_dto = user_db.get_by_username(token.username)
    
    if not user_dto:
        raise HTTPException(status_code=400, detail="User not found")

    # ItemResponse is the model it will map to.
    return item_db.get(user_dto.id, skip, limit)




