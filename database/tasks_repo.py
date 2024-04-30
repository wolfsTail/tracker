from database.base_repo import BaseRepo

from database.database import get_db_connection


class TasksRepo(BaseRepo):
    TABLE_NAME = "Tasks"

    @classmethod
    def add_task(cls, **kwargs):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"INSERT INTO Tasks (id, name, time_periods, category_id) VALUES (?, ?, ?, ?)",
                (kwargs["id"],kwargs["name"], kwargs["time_periods"], kwargs["category_id"]),
            )
            conn.commit()
    
    @classmethod
    def update_task(cls, **kwargs):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE Tasks SET name = ?, time_periods = ?, category_id = ? WHERE id = ?",
                (kwargs["name"], kwargs["time_periods"], kwargs["category_id"], kwargs["id"]),
            )
            conn.commit()