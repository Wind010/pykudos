from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: Optional[str] = None
    firstname: Optional[str]= None
    lastname: Optional[str]= None
    disabled: Optional[str] = None
