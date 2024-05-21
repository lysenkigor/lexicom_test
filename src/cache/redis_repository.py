from functools import lru_cache

from fastapi import Depends
from redis.asyncio import Redis

from src.cache.redis_connection import get_redis


class RedisRepository:
    """
    A repository class that uses Redis as its data store.

    Args:
        connection (Redis): A Redis connection object.

    Attributes:
        _connection(Redis): A Redis connection object.
    """

    def __init__(self, connection: Redis):
        self._connection: Redis = connection

    async def get(self, key: str) -> str:
        return await self._connection.get(key)

    async def put(self, key: str, value: str) -> None:
        await self._connection.set(key, value)


@lru_cache()
def get_cache_repo(
        redis: Redis = Depends(get_redis)
) -> RedisRepository:
    return RedisRepository(redis)
