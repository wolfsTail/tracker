from schemas import Task, ResponseTask

from utils import AbstractUnitOfWork


class TaskService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def get_one_task(self, task_id: int):
        async with self.uow:
            task = await self.uow.tasks.get_one(task_id, self.uow.session)
            if task:
                return ResponseTask.model_validate(task)
            return None

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
    
    async def update_task(self, task_id: int, task: Task) -> ResponseTask:
        task_dict: dict = task.model_dump()
        async with self.uow:
            task_updated = await self.uow.tasks.update_one(task_id, self.uow.session, task_dict)       

            if task_updated:
                task_from_bd = task_updated.model_validate(task)
                await self.uow.commit()
                return task_from_bd        
        return None
    
    async def delete_one(self, task_id: int):
        async with self.uow:
            success = self.uow.tasks.delete_one(task_id, self.uow.session)
            if success:
                self.uow.commit()
                return 1
            return None

