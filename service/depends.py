from fastapi import Depends

from service.task_service import TaskService
from service.category_service import CategoryService
from utils.unitofwork import AbstractUnitOfWork, UnitOfWork
from repository import TaskCache
from cache import get_redis_connection


async def get_task_service(uow: AbstractUnitOfWork = Depends(UnitOfWork)) -> TaskService:
    return TaskService(uow)


async def get_category_service(uow: AbstractUnitOfWork = Depends(UnitOfWork)) -> CategoryService:
    return CategoryService(uow)


def get_task_cache_repo() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)
