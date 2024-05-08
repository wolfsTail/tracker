from fastapi import Depends

from service.task_service import TaskService
from service.category_service import CategoryService
from utils.unitofwork import AbstractUnitOfWork, UnitOfWork


async def get_task_service(uow: AbstractUnitOfWork = Depends(UnitOfWork)) -> TaskService:
    return TaskService(uow)


async def get_category_service(uow: AbstractUnitOfWork = Depends(UnitOfWork)) -> CategoryService:
    return CategoryService(uow)
