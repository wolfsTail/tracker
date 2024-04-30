import sqlite3

from core.settings import settings


def get_db_connection() -> sqlite3.Connection:
    return sqlite3.connect(settings.DB_NAME)