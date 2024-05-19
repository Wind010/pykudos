from abc import ABC, abstractmethod
from typing import Any, Dict, Union
from uuid import UUID
from database.models.user import User

from database.schemas.user import UserCreateRequest

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
    def get_by_external_id(self, external_user_id: Union[UUID, str]) -> User:
        pass

    @abstractmethod
    def create(self, user: UserCreateRequest, hashed_password: str):
        pass