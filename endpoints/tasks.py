from typing import Annotated

from fastapi import APIRouter, status, HTTPException

from fixtures import tasks as fixture_tasks
from database.tasks_repo import TasksRepo
from schemas.task import Task, ResponseTask


router = APIRouter(prefix="/tasks", tags=["tasks",])


@router.get(
        path="/all", response_model=list[ResponseTask]
        )
async def get_all_tasks():
    tasks = []
    result = TasksRepo.get_all()
    for task in result:
        tasks.append(
            ResponseTask(
                id=task[0],
                name=task[1],
                time_periods=task[2],
                category_id=task[3],
            )
        )
    return tasks


@router.post(
        path="/", response_model=ResponseTask
        )
async def create_task(task: ResponseTask):
    TasksRepo.add_task(
        id=task.id,
        name=task.name,
        time_periods=task.time_periods,
        category_id=task.category_id
    )   
    return task


@router.patch(
        path="/{task_id}", 
        response_model=ResponseTask,
        status_code=status.HTTP_202_ACCEPTED
        )
async def update_task(task_id: int, task:Task):
    TasksRepo.update_task(
        id=task_id,
        name=task.name,
        time_periods=task.time_periods,
        category_id=task.category_id
    )


@router.delete(
        path="/{task_id}",
        status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task(task_id: int):
    result = TasksRepo.delete(task_id)
    if result:
        raise HTTPException(status_code=404, detail="task not found")
