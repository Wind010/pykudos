from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from jose import JWTError, jwt
from passlib.context import CryptContext

from common.config import Settings
from database.models.user import User

from database.user_datalayer import UserDatalayer

from models.common.token import Token, TokenData


settings = Settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def get_db(request: Request) -> Session:
    return request.state.db


#db: Session = Depends(get_db)
def authenticate_user(login: str, password: str, db: Session = Depends(get_db)) -> Optional[User]:
    #user = User().with_data_repository()
    crud = UserDatalayer(db)
    if '@' in login:
        user_dto: User = crud.get_by_email(login)
    else:
        user_dto: User = crud.get_by_username(login)
 
    if not user_dto:
        return None

    hashed_password: str = get_password_hash(password)
    if not verify_password(password, hashed_password):
        return None
    
    return user_dto


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     user = User().with_data_repository()
#     hashed_password: str = user.decode_token(token)
#     if not hashed_password:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return hashed_password
 

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
        
    crud = UserDatalayer(db)
    user_dto: User = crud.get_by_username(token_data.username)

    if user_dto is None:
        raise credentials_exception
    return user_dto


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_admin_user(current_user: Annotated[User, Depends(get_current_active_user)]) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=400, detail="Not admin!")
    return current_user

