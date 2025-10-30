from .user import get_user_by_email, create_user
from .note import create_note, update_note, delete_note, get_note, search_notes
from .tag import create_tag, get_tags, update_tag, delete_tag, add_tag_to_note, remove_tag_from_note
from .favorite import add_favorite, remove_favorite, get_user_favorite_notes, is_note_favorited, list_notes_with_favorites

__all__ = [
    "get_user_by_email", "create_user", "create_note", "update_note",
    "delete_note", "get_note", "search_notes", "create_tag", "get_tags",
    "update_tag", "delete_tag", "add_tag_to_note", "remove_tag_from_note",
    "add_favorite", "remove_favorite", "get_user_favorite_notes",
    "is_note_favorited", "list_notes_with_favorites"
]
