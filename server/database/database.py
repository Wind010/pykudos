from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from common.config import Settings
from common.constants import SQL_LITE

settings = Settings()


SQLALCHEMY_DATABASE_URL = settings.database_connection_string

check_same_thread: bool = True
if settings.database_type == SQL_LITE:
    check_same_thread = False

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": check_same_thread}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()