# -*- coding: utf-8 -*-
# @Time        : 2025-08-18 14:36:34
# @Author      : gaochenyang
# @File        : tag.py
# @Description :

# here put the import lib
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base
from app.models.note_tags import note_tags


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    notes = relationship("Note", secondary=note_tags, back_populates="tags")
