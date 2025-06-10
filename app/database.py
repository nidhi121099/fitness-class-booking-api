from app.models import Database

_db = None

def get_db():
    global _db
    if _db is None:
        _db = Database()
    return _db