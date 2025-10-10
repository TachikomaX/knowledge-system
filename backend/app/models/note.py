# -*- coding: utf-8 -*-
# @Time        : 2025-08-18 14:36:07
# @Author      : gaochenyang
# @File        : note.py
# @Description :

# here put the import lib
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db import Base
from app.models.note_tags import note_tags


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(),
                        onupdate=func.now())

    # 全文搜索字段
    search_vector = Column(TSVECTOR)

    user = relationship("User", backref="notes")
    tags = relationship("Tag", secondary=note_tags, back_populates="notes")
    favorites = relationship("Favorite",
                             back_populates="note",
                             cascade="all, delete-orphan")
