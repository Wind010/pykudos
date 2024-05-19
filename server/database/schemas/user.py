from uuid import UUID
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from database.schemas.item import Item

import re 





class UserBase(BaseModel):
    email: str = Field(..., min_length=4, max_length=320, pattern=r'[^@]+@[^@]+\.[^@]+')
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=100)
    username: str = Field(..., min_length=3, max_length=20)
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, value):
        if not value.isalnum():
            raise ValueError('Username must be alphanumeric')
        return value
    

class User(UserBase):
    """Domain object"""
    id: int
    external_id: UUID
    is_active: bool
    is_admin: bool
    date_created: datetime
    date_modified: datetime
    items: list[Item] = []

    class Config:
        orm_mode = True


class UserCreateRequest(UserBase):
    password: str = Field(..., min_length=10)

    # Workaround for https://github.com/pydantic/pydantic/issues/7058
    @field_validator("password")
    @classmethod
    def regex_match(cls, p: str) -> str:
        # Minimum of 10 characters, at least one uppercase letter, one lowercase letter, and one number, 
        # and one special character.
        #PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{10,}$"
        PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{10,}$"
        re_for_pw = re.compile(PASSWORD_REGEX)

        if not re_for_pw.match(p):
            raise ValueError("Invalid Password. Minimum of 10 characters, at least one uppercase letter, one lowercase letter, one number and one special character")
        return p


class UserResponse(UserBase):
    pass