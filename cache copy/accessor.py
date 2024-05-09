from redis import Redis

from core import settings


def get_redis_connection() -> Redis:
    return Redis(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
        )
