from typing import List, Union
from uuid import UUID
from sqlalchemy.orm import Session

from database.abstract_user_base_repository import AbstractUserBaseRepository
from database.models.user import User

class UserDatalayer(AbstractUserBaseRepository):

    def __init__(self, db: Session):
        self.__session = db

    def get_by_id(self, id: int) -> User:
        """Internal use only"""
        return self.__session.query(User).filter(User.id == id).first()

    def get_by_external_id(self, external_user_id: Union[UUID, str]) -> User:
        return self.__session.query(User).filter(User.external_id == external_user_id).first()

    def get_by_username(self, username: str) -> User:
        return self.__session.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> User:
        return self.__session.query(User).filter(User.email == email).first()

    def get_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.__session.query(User).offset(skip).limit(limit).all()

    def create(self, user: User, hashed_password: str) -> User:
        db: Session = self.__session
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

