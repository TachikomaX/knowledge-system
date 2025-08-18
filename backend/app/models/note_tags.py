# -*- coding: utf-8 -*-
# @Time        : 2025-08-18 14:37:08
# @Author      : gaochenyang
# @File        : note_tags.py
# @Description :

# here put the import lib
from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db import Base

note_tags = Table(
    "note_tags", Base.metadata,
    Column("note_id", Integer, ForeignKey("notes.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True))
