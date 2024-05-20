import json
from redis import asyncio as Redis

from fastapi import Depends

from repository.cache_base_repo import BaseCacheRepo
from cache import get_redis_connection
from schemas import ResponseTask


class TaskCache(BaseCacheRepo):
    cache: Redis = get_redis_connection
    model = ResponseTask

    @classmethod
    async def get_list_items(cls) -> list[ResponseTask]:
        async with cls.cache() as redis:
            result_json = await redis.lrange("tasks", 0, -1)
            return [cls.model.model_validate(json.loads(task)) for task in result_json]
        
    @classmethod
    async def set_list_items(cls, items: list[ResponseTask]):
        tasks_json = [task.model_dump_json() for task in items]
        async with cls.cache() as redis:
            await redis.delete("tasks")
            await redis.lpush("tasks", *tasks_json)
            await redis.expire("tasks", 60)
    
    @classmethod
    async def get_item(cls, task_id: int)-> ResponseTask:
        async with cls.cache() as redis:
            task_json = await redis.get(str(task_id))
            if task_json:
                return cls.model.model_validate(json.loads(task_json))
    
    @classmethod
    async def set_item(cls, task: ResponseTask):
        async with cls.cache() as redis:
            await redis.set(str(task.id), task.model_dump_json(), 30)
