from abc import ABC, abstractmethod
from typing import Any, Dict

from database.schemas.user import UserCreate

class AbstractUserBaseRepository(ABC):

    @abstractmethod
    def get_by_id(self, username: str) -> Dict[str, Any]:
        pass

    # @abstractmethod
    # def get_by_username(self, username: str) -> Dict[str, Any]:
    #     pass

    def get_by_email(self, user_id: int):
        pass

    @abstractmethod
    def get_users(self, skip: int = 0, limit: int = 100):
        pass

    @abstractmethod
    def create(self, user: UserCreate, hashed_password: str):
        pass