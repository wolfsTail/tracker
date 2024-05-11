import json
from redis import Redis

from fastapi import Depends

from repository.cache_base_repo import BaseCacheRepo
from cache import get_redis_connection
from schemas import ResponseCategory


class CategoryCache(BaseCacheRepo):
    cache: Redis = get_redis_connection
    model = ResponseCategory

    @classmethod
    def get_list_items(cls) -> list[ResponseCategory]:
        with cls.cache() as redis:
            result_json = redis.lrange("categories", 0, -1)
            return [cls.model.model_validate(json.loads(category)) for category in result_json]

    @classmethod
    def set_list_items(cls, items: list[ResponseCategory]):
        categories_json = [category.model_dump_json() for category in items]
        with cls.cache() as redis:
            redis.delete("categories")
            redis.lpush("categories", *categories_json)
            redis.expire("categories", 60)

    @classmethod
    def get_item(cls, category_id: int)-> ResponseCategory:
        with cls.cache() as redis:
            category_json = redis.get(str(category_id))
            if category_json:
                return cls.model.model_validate(json.loads(category_json))
    
    @classmethod
    def set_item(cls, category: ResponseCategory):
        with cls.cache() as redis:
            redis.set(str(category.id), category.model_dump_json(), 30)
    