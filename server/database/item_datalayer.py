from sqlalchemy.orm import Session
from database.database import SessionLocal
from database.models.item import Item
from database.schemas.item import ItemCreate


class ItemDatalayer():
    def __init__(self, db: Session):
        self.__session = db

    def get_items(self, skip: int = 0, limit: int = 100):
        return self.__session.query(Item).offset(skip).limit(limit).all()


    def create_user_item(self, item: ItemCreate, user_id: int):
        db = self.__session
        db_item = Item(**item.model_dump(), owner_id=user_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item