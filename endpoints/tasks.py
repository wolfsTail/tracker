from fastapi import APIRouter, status, HTTPException, Depends

from schemas.task import Task, ResponseTask
from service.depends import TaskService, get_task_service, TaskCache


router = APIRouter(prefix="/tasks", tags=["tasks",])


@router.get("/all", response_model=list[Task])
async def get_all_tasks(
    tasks_service: TaskService = Depends(get_task_service)    
):
    tasks = await tasks_service.get_all_tasks()
    if not tasks:
        raise HTTPException(status_code=404, detail="Не найдено ни одной задачи")
    return tasks


@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: int, 
    tasks_service: TaskService = Depends(get_task_service),
):
    task = await tasks_service.get_one_task(task_id)

    if not task:
        raise HTTPException(status_code=404, detail=f"Не найдено задачи с {task_id=}")
    return task


@router.post("/", response_model=ResponseTask)
async def create_task(
    task: Task, tasks_service: TaskService = Depends(get_task_service)
    ):
    return await tasks_service.create_task(task)


@router.patch("/", response_model=ResponseTask, status_code=status.HTTP_202_ACCEPTED)
async def update_task(
    task_id: int, task: Task, tasks_service: TaskService = Depends(get_task_service)
):
    return await tasks_service.update_task(task_id, task)


@router.delete(path="/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int, tasks_service: TaskService = Depends(get_task_service)
):
    result = await tasks_service.delete_one(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="task not found")
    return None
