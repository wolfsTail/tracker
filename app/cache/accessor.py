from redis import asyncio as redis
from redis import Redis

from app.core import settings


REDIS_URL = settings.REDIS_URL

def get_redis_connection() -> Redis:
    return redis.from_url(url=REDIS_URL)
