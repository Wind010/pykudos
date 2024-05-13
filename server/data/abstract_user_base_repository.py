from abc import ABC, abstractmethod
from typing import Any, Dict

class AbstractUserBaseRepository(ABC):

    @abstractmethod
    def get(self, username: str) -> Dict[str, Any]:
        pass

    def add(self, user: Dict[str, Any]) -> bool:
        pass