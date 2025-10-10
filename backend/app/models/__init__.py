# app/models/__init__.py
from app.models.note import Note
from app.models.note_tags import note_tags
from app.models.tag import Tag
from app.models.user import User
from app.models.favorite import Favorite


__all__ = ["User", "Note", "Tag", "note_tags", "Favorite"]
