from schemas import Task, Category, ResponseCategory, ResponseTask

from utils import UnitOfWork, AbstractUnitOfWork


class TaskService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def get_all_tasks(self) -> list[ResponseTask]:
        async with self.uow:
            tasks = await self.uow.tasks.get_all(self.uow.session)
            return [ResponseTask.model_validate(task) for task in tasks]
    
    async def create_task(self, task: Task) -> ResponseTask:
        task_dict: dict = task.model_dump()
        async with self.uow:
            task = await self.uow.tasks.create_one(task_dict, self.uow.session)
            task_from_db = ResponseTask.model_validate(task)
            await self.uow.commit()
            return task_from_db