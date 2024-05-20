from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    is_oppertunity = Column(String, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    date_created = Column(DateTime(timezone=True), server_default=func.now()) # Server should be UTC.
    date_modified = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="items")