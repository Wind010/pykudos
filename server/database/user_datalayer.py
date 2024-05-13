from sqlalchemy.orm import Session

from database.abstract_user_base_repository import AbstractUserBaseRepository
from database.database import SessionLocal
from database.models.user import User
from database.schemas.user import UserCreate


class UserDatalayer(AbstractUserBaseRepository):

    def __init__(self, db: Session):
        self.__session = db

    def get_by_id(self, user_id: int):
        return self.__session.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str):
        return self.__session.query(User).filter(User.email == email).first()

    def get_users(self, skip: int = 0, limit: int = 100):
        return self.__session.query(User).offset(skip).limit(limit).all()

    def create(self, user: UserCreate, hashed_password: str):
        db: Session = self.__session
        db_user = User(email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

