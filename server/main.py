import uvicorn
from fastapi import Depends, FastAPI
from fastapi.templating import Jinja2Templates

#from .dependencies import get_query_token, get_token_header
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware


#from .internal import admin
from common.config import Settings
from common.constants import DEV
from middleware.db_session_middleware import DbSessionMiddleware
from routers import admin, auth, items, pages, users

#app = FastAPI(dependencies=[Depends(get_query_token)])

settings = Settings()
IS_DEVELOPMENT: bool = settings.environment == DEV

app = FastAPI(debug=IS_DEVELOPMENT)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(DbSessionMiddleware)
#app.add_middleware(HTTPSRedirectMiddleware)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(pages.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(oauth2_scheme)],
    responses={418: {"description": "I'm a teapot"}},
)

templates = Jinja2Templates(directory="templates")


if __name__ == "__main__":
    if IS_DEVELOPMENT:
        uvicorn.run(app, host="0.0.0.0", port=8000)