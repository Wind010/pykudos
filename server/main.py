import uvicorn
from fastapi import Depends, FastAPI


#from .dependencies import get_query_token, get_token_header
from fastapi.security import OAuth2PasswordBearer

#from .internal import admin
from common.config import Settings
from common.constants import DEV
from routers import auth, users, admin

#app = FastAPI(dependencies=[Depends(get_query_token)])

settings = Settings()
IS_DEVELOPMENT: bool = settings.environment == DEV

app = FastAPI(debug=IS_DEVELOPMENT)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app.include_router(auth.router)

app.include_router(users.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(oauth2_scheme)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Root!"}


if __name__ == "__main__":
    if settings.environment == IS_DEVELOPMENT:
        uvicorn.run(app, host="0.0.0.0", port=8000)