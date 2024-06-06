from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from jose import JWTError, jwt
from passlib.context import CryptContext

from common.config import Settings
from database.database import SessionLocal
from database.models.user import User

from database.user_datalayer import UserDatalayer

from models.common.token import Token, TokenData


settings = Settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

COULD_NOT_VERIFY_CREDENTIALS = "Could not validate credentials"

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


# Since we've abstracted get_current_user here we need to resolve directly instead of middleware. 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

 
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


def get_or_create_user(db: Session, username: str, email: str) -> Optional[User]:
    crud = UserDatalayer(db)
    user_dto: User = crud.get_by_username(username)
    if not user_dto:
        user_dto = User()
        user_dto.username = username
        user_dto.email = email
        user_dto = crud.create(user_dto, email)
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


def decode_access_token(token: str) -> TokenData:
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    username: str = payload.get("sub")
    return TokenData(username=username)
    


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
 


def get_token(request: Request):
    """
    Resolves the access token from the cookie or from the request header.
    """
    token: str = get_token_from_cookie(request)
    if not token:
        token = oauth2_scheme(request)
    return token
    

def get_token_from_cookie(request: Request):
    """
    Will be provided by the template pages hosted by server.
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

async def get_current_user(token: Annotated[str, Depends(get_token)], db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=COULD_NOT_VERIFY_CREDENTIALS,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_data: TokenData = decode_access_token(token)
        crud = UserDatalayer(db)
        user_dto: User = crud.get_by_username(token_data.username)

        if user_dto is None:
            raise credentials_exception
        return user_dto
    except JWTError:
        raise credentials_exception
        


async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_admin_user(current_user: Annotated[User, Depends(get_current_active_user)]) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=400, detail="Not admin!")
    return current_user

