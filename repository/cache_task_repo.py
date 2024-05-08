import json
from redis import Redis

from schemas import Task, ResponseTask


class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_tasks(self) -> list[ResponseTask]:
        with self.redis as redis:
            result_json = redis.lrange("tasks", 0, -1)
            return [ResponseTask.model_validate(json.loads(task)) for task in result_json]

        

    def set_tasks(self, tasks: list[Task]):
        tasks_json = [task.model_dump_json() for task in tasks]
        with self.redis as redis:
            redis.lpush("tasks", *tasks_json)
