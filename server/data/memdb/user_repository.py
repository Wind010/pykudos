from typing import Any, Dict
from data.memdb.db import DB

from data.abstract_user_base_repository import AbstractUserBaseRepository


class InMemoryDb(AbstractUserBaseRepository):
    """
    In-memory database and datalayer.
    """

    @staticmethod
    def get(username: str) -> Dict[str, Any]:
        if username in DB:
            user_dict = DB[username]
            return user_dict

    @staticmethod
    def add(user: Dict[str, Any]) -> bool:
        DB.update(user)
        return True
