from redis import Redis

from core import settings


REDIS_URL = settings.REDIS_URL

def get_redis_connection() -> Redis:
    return Redis(url=REDIS_URL)
