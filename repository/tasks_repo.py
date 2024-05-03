from database.models import Tasks, Categories
from repository.base_repo import BaseRepo

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from fastapi import Depends
from typing import Annotated


class TaskRepository(BaseRepo):
    model_name = Tasks

    @classmethod
    async def get_tasks_by_category_name(
        cls, db_session: AsyncSession, category_name: str
        ) -> list[Tasks]:
        stmt = select(cls.model_name).join(Categories, Categories.id == Tasks.category_id)\
        .where(Categories.name == category_name)
        result = await db_session.execute(stmt)
        return result.scalars().all()
