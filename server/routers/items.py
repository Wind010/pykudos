from typing import Annotated
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from database.database import SessionLocal, engine

from database.models.item import Item as ItemModel
from database.schemas.item import Item as ItemSchema, ItemCreateRequest


from database.item_datalayer import ItemDatalayer
from database.user_datalayer import UserDatalayer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Dependency
def get_db(request: Request):
    return request.state.db


@router.post("/items/", response_model=int, tags=["users"])
def create_item(item: ItemCreateRequest, db: Session = Depends(get_db)):
    user_db, item_db = UserDatalayer(db), ItemDatalayer(db)
    
    #TODO:  Validate expected user with token.

    db_user = user_db.get_by_external_id(item.user_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User not found.")
    
    db_item = item_db.create(item=item)

    return db_item.id



@router.get("/items/", response_model=list[ItemSchema], tags=["items"])
async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    crud = ItemDatalayer(db)
    items = crud.get(db, skip=skip, limit=limit)
    return items


