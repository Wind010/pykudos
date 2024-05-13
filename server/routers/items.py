from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/items/", tags=["items"])
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}