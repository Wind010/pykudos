from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    external_id = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    date_created = Column(DateTime(timezone=True), server_default=func.now()) # Server should be UTC.
    date_modified = Column(DateTime(timezone=True),  server_default=func.now(), onupdate=func.now())


    # backref="id"
    items = relationship("Item", back_populates="user")

