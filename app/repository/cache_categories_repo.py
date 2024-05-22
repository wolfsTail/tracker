import json
from redis import asyncio as Redis

from app.repository.cache_base_repo import BaseCacheRepo
from app.cache import get_redis_connection
from app.schemas import ResponseCategory


class CategoryCache(BaseCacheRepo):
    cache: Redis = get_redis_connection
    model = ResponseCategory

    @classmethod
    async def get_list_items(cls) -> list[ResponseCategory]:
        async with cls.cache() as redis:
            result_json = await redis.lrange("categories", 0, -1)
            return [cls.model.model_validate(json.loads(category)) for category in result_json]

    @classmethod
    async def set_list_items(cls, items: list[ResponseCategory]):
        categories_json = [category.model_dump_json() for category in items]
        async with cls.cache() as redis:
            await redis.delete("categories")
            await redis.lpush("categories", *categories_json)
            await redis.expire("categories", 60)

    @classmethod
    async def get_item(cls, category_id: int)-> ResponseCategory:
        async with cls.cache() as redis:
            category_json = await redis.get(str(category_id))
            if category_json:
                return cls.model.model_validate(json.loads(category_json))
    
    @classmethod
    async def set_item(cls, category: ResponseCategory):
        async with cls.cache() as redis:
            await redis.set(str(category.id), category.model_dump_json(), 30)
    