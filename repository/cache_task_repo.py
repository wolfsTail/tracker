import json
from redis import Redis

from fastapi import Depends

from repository.cache_base_repo import BaseCacheRepo
from cache import get_redis_connection
from schemas import ResponseTask


class TaskCache(BaseCacheRepo):
    cache: Redis = Depends(get_redis_connection)
    model = ResponseTask

    @classmethod
    def get_list_items(cls) -> list[ResponseTask]:
        with cls.cache as redis:
            result_json = redis.lrange("tasks", 0, -1)
            return [cls.model.model_validate(json.loads(task)) for task in result_json]
        
    @classmethod
    def set_list_items(cls, items: list[ResponseTask]):
        tasks_json = [task.model_dump_json() for task in items]
        with cls.cache as redis:
            redis.delete("tasks")
            redis.lpush("tasks", *tasks_json)
            redis.expire("tasks", 60)
    
    @classmethod
    def get_item(cls, task_id: int)-> ResponseTask:
        with cls.cache as redis:
            task_json = redis.get(str(task_id))
            if task_json:
                return cls.model.model_validate(json.loads(task_json))
    
    @classmethod
    def set_item(cls, task: ResponseTask):
        with cls.cache as redis:
            redis.set(str(task.id), task.model_dump_json(), 30)
