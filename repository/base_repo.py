from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update
from fastapi import Depends
from typing import Annotated
from database.database import get_db_session as AsyncSessionLocal


class BaseRepo:
    model_name = None

    @classmethod
    async def get_all(
        cls, db: Annotated[AsyncSession, Depends(AsyncSessionLocal)]
        ) -> list[model_name]:
        async with db() as session:
            stmt = select(cls.model_name)
            result = await session.execute(stmt)
            return result.scalars().all()

    @classmethod
    async def get_one(
        cls, item_id, db: Annotated[AsyncSession, Depends(AsyncSessionLocal)]
        ) -> model_name:
        async with db() as session:
            stmt = select(cls.model_name).filter_by(id=item_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @classmethod
    async def create_one(
        cls, db: Annotated[AsyncSession, Depends(AsyncSessionLocal)], **kwargs
        ) -> model_name:
        async with db() as session:
            item = cls.model_name(**kwargs)
            session.add(item)
            await session.commit()
            return item

    @classmethod
    async def update_one(
        cls, item_id, db: AsyncSession, **kwargs
        ) -> model_name | None:
        async with db() as session:
            stmt = (
                update(cls.model_name)
                .where(cls.model_name.id == item_id)
                .values(**kwargs)
                .returning(cls.model_name)
            )
            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    @classmethod
    async def delete_one(cls, item_id, db: AsyncSession) -> bool:
        async with db() as session:
            stmt = delete(cls.model_name).where(cls.model_name.id == item_id)
            result = await session.execute(stmt)
            return bool(result.rowcount)
