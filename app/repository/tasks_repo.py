from app.models import Tasks, Categories
from app.repository.base_repo import BaseRepo

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update


class TaskRepository(BaseRepo):
    model_name = Tasks

    @classmethod
    async def get_one(
        cls, item_id: int, user_id: int, db_session: AsyncSession
        ) -> model_name:
        stmt = select(cls.model_name).filter_by(id=item_id, user_id=user_id)
        result = await db_session.execute(stmt)
        return result.scalar_one_or_none()

    @classmethod
    async def get_all(
        cls, db_session: AsyncSession, user_id: int
        ) -> list[model_name]:
        stmt = select(cls.model_name).where(cls.model_name.user_id == user_id)
        result = await db_session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def get_tasks_by_category_name(
        cls, db_session: AsyncSession, category_name: str
        ) -> list[Tasks]:
        stmt = select(cls.model_name).join(Categories, Categories.id == Tasks.category_id)\
        .where(Categories.name == category_name)
        result = await db_session.execute(stmt)
        return result.scalars().all()
    
    @classmethod
    async def delete_one(
        cls, item_id: int, user_id: int, db_session: AsyncSession
        ) -> bool:
        stmt = delete(cls.model_name).where(cls.model_name.id == item_id,
                                            cls.model_name.user_id == user_id)
        result = await db_session.execute(stmt)
        return bool(result.rowcount)
