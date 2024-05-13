from typing import Annotated
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from database.database import SessionLocal, engine

from database.models.item import Item as ItemModel
from database.schemas.item import item as ItemSchema, ItemCreate


from database.item_datalayer import ItemDatalayer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




# Dependency
def get_db(request: Request):
    return request.state.db



@router.get("/items/", response_model=list[ItemSchema], tags=["items"])
async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    crud = ItemDatalayer(db)
    items = crud.get_items(db, skip=skip, limit=limit)
    return items