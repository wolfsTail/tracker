from fastapi import Depends

from service.task_service import TaskService
from utils.unitofwork import AbstractUnitOfWork, UnitOfWork


async def get_task_service(uow: AbstractUnitOfWork = Depends(UnitOfWork)) -> TaskService:
    return TaskService(uow)
