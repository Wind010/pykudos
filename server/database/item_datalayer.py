from sqlalchemy.orm import Session
from database.models.item import Item
from database.schemas.item import ItemCreateRequest


class ItemDatalayer():
    def __init__(self, db: Session):
        self.__session = db

    def get(self, skip: int = 0, limit: int = 100):
        return self.__session.query(Item).offset(skip).limit(limit).all()
    
    def delete(self, id: int):
        # TODO:  Handle exception and logging.  Add return type.
        db = self.__session
        item = db.query(Item).filter(Item.id == id).first()
        db.delete(item)
        
    def create(self, item: ItemCreateRequest):
        db = self.__session
        db_item = Item(**item.model_dump(), user_id=item.user_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    