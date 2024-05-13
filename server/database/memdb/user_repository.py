from typing import Any, Dict
from database.memdb.db import DB

from database.abstract_user_base_repository import AbstractUserBaseRepository


class InMemoryDb(AbstractUserBaseRepository):
    """
    In-memory database and datalayer.
    """

    @staticmethod
    def get_by_email(email: str) -> Dict[str, Any]:
        if email in DB:
            user_dict = DB[email]
            return user_dict

    @staticmethod
    def create(user: Dict[str, Any]) -> bool:
        DB.update(user)
        return True
