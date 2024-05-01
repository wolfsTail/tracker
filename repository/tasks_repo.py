from database.models import Tasks, Categories
from repository.base_repo import BaseRepo

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from fastapi import Depends
from typing import Annotated
from database.database import get_db_session as AsyncSessionLocal


class TaskRepository(BaseRepo):
    model_name = Tasks

    @classmethod
    async def get_tasks_by_category_name(
        cls, db: Annotated[AsyncSession, Depends(AsyncSessionLocal)], category_name: str
        ) -> list[model_name]:
        async with db() as session:
            stmt = select(cls.model_name).join(Categories, Categories.id == Tasks.category_id)\
            .where(Categories.name == category_name)
            result = await session.execute(stmt)
            return result.scalars().all()
