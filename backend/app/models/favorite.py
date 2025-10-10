from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from app.db import Base


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    note_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="favorites")
    note = relationship("Note", back_populates="favorites")
