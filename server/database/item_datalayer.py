from typing import List
from sqlalchemy.orm import Session
from database.models.item import Item


class ItemDatalayer():
    def __init__(self, db: Session):
        self.__session = db

    def get(self, user_id: int,  skip: int = 0, limit: int = 100) -> List[Item]:
        return self.__session.query(Item).filter(Item.user_id == user_id).offset(skip).limit(limit).all()
    
    def delete(self, id: int):
        # TODO:  Handle exception and logging.  Add return type.
        db = self.__session
        item = db.query(Item).filter(Item.id == id).first()
        db.delete(item)
        
    def create(self, item: Item) -> Item:
        db = self.__session
        db.add(item)
        db.commit()
        db.refresh(item)
        return item
    