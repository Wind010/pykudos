from fastapi import Request, Response
from database.database import SessionLocal
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class DbSessionMiddleware(BaseHTTPMiddleware):
    
    # https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-middleware
    # https://www.starlette.io/middleware/#sessionmiddleware
    
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self.db = SessionLocal()

    async def dispatch(self, request: Request, call_next):
        response = Response("Internal server error", status_code=500)
        try:
            request.state.db = self.db
            response = await call_next(request)
        finally:
            request.state.db.close()
        return response
