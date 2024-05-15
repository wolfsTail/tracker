from schemas import Task, ResponseTask

from utils import AbstractUnitOfWork


class TaskService:
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def get_one_task(self, task_id: int, user_id: int):
        async with self.uow:
            if task := self.uow.cache_tasks.get_item(task_id):
                return task
            task = await self.uow.tasks.get_one(task_id, user_id, self.uow.session)
            if task:
                response_task = ResponseTask.model_validate(task)
                self.uow.cache_tasks.set_item(response_task)
                return response_task
            return None

    async def get_all_tasks(self, user_id: int) -> list[ResponseTask]:
        async with self.uow:
            if tasks := self.uow.cache_tasks.get_list_items():
                return tasks            
            tasks = await self.uow.tasks.get_all(self.uow.session, user_id)
            if tasks:
                response_tasks = [ResponseTask.model_validate(task) for task in tasks]
                self.uow.cache_tasks.set_list_items(response_tasks)
                return response_tasks
    
    async def create_task(
            self, task: Task, user_id: int
            ) -> ResponseTask:
        task_dict: dict = task.model_dump()
        task_dict.update(
            {"user_id": user_id}
        )
        async with self.uow:
            task = await self.uow.tasks.create_one(task_dict, self.uow.session)
            task_from_db = ResponseTask.model_validate(task)
            await self.uow.commit()
            return task_from_db
    
    async def update_task(
            self, task_id: int, task: Task, user_id: int
            ) -> ResponseTask:
        task_dict: dict = task.model_dump()
        task_dict.update(
            {"user_id": user_id}
        )
        async with self.uow:
            task_updated = await self.uow.tasks.update_one(task_id, self.uow.session, task_dict)       

            if task_updated:
                task_from_bd = task_updated.model_validate(task)
                await self.uow.commit()
                return task_from_bd        
        return None
    
    async def delete_one(self, task_id: int, user_id: int):
        async with self.uow:
            success = self.uow.tasks.delete_one(task_id, user_id, self.uow.session)
            if success:
                self.uow.commit()
                return 1
            return None

