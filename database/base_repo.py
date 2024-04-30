import sqlite3

from database.database import get_db_connection


class BaseRepo:
    TABLE_NAME = None
    @classmethod
    def get_all(cls):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {cls.TABLE_NAME}")
            return cursor.fetchall()
    
    @classmethod
    def get_one_or_none(cls, id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {cls.TABLE_NAME} WHERE id = ?", (id,))
            return cursor.fetchone()
    
    @classmethod
    def delete(cls, id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {cls.TABLE_NAME} WHERE id = ?", (id,))

