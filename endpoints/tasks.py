from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends

from repository import TaskRepository
from schemas.task import Task, ResponseTask
from sqlalchemy.ext.asyncio import AsyncSession
from service.depends import TaskService, get_task_service


router = APIRouter(prefix="/tasks", tags=["tasks",])


@router.get("/all", response_model=list[Task])
async def get_all_tasks(
    tasks_service: TaskService = Depends(get_task_service)
):
    tasks = await tasks_service.get_all_tasks()
    if not tasks:
        raise HTTPException(status_code=404, detail="Не найдено ни одной задачи")
    return tasks


@router.post("/", response_model=ResponseTask)
async def create_task(
    task: Task, tasks_service: TaskService = Depends(get_task_service)
    ):
    return await tasks_service.create_task(task)


# @router.post(
#         path="/", response_model=ResponseTask
#         )
# async def create_task(task: ResponseTask):
#     TasksRepo.add_task(
#         id=task.id,
#         name=task.name,
#         time_periods=task.time_periods,
#         category_id=task.category_id
#     )   
#     return task


# @router.patch(
#         path="/{task_id}", 
#         response_model=ResponseTask,
#         status_code=status.HTTP_202_ACCEPTED
#         )
# async def update_task(task_id: int, task:Task):
#     TasksRepo.update_task(
#         id=task_id,
#         name=task.name,
#         time_periods=task.time_periods,
#         category_id=task.category_id
#     )


# @router.delete(
#         path="/{task_id}",
#         status_code=status.HTTP_204_NO_CONTENT
# )
# async def delete_task(task_id: int):
#     result = TasksRepo.delete(task_id)
#     if result:
#         raise HTTPException(status_code=404, detail="task not found")
