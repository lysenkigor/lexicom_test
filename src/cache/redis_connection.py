from redis.asyncio import Redis

from src.core.config import settings

redis: Redis = Redis.from_url(settings.redis_url)


async def get_redis() -> Redis:
    return redis
