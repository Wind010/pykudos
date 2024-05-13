from typing import Any, Dict
from database.memdb.user_repository import InMemoryDb

class DomainUser():
    """
    Shim to the data repository.
    """

    valid_keys = {'username', 'email', 'firstname', 'lastname', 'disabled', 'is_admin'}

    def __init__(self, **kwargs):
        self.username: str = None

        for key, value in kwargs.items():
            if key in DomainUser.valid_keys:
                setattr(self, key, value)

        self.hashed_password = ''
        self.data_store_type = 'memory'
        self.repo = InMemoryDb()

    def with_data_repository(self, data_store_type: str = 'memory'):
        self.data_store_type = data_store_type

        if data_store_type == 'memory':
            self.repo = InMemoryDb()
            
        return self
    
    def get(self, username: str) -> 'DomainUser':
        user: Dict[str, Any] = self.repo.get(username)
        loaded_user = DomainUser(**user)
        self.__dict__.update(loaded_user.__dict__)

        # Be explicit with sensitive fields.
        #self.hashed_password = user['hashed_password']
        return self

    def add(self) -> bool:
        self.repo.add(self)


    def decode_token(self, token) -> str:
        if not self.hashed_password:
            self.get(token)
        return self.hashed_password

