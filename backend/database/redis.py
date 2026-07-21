from redis.asyncio import Redis, ConnectionPool
from backend.config.settings import settings

pool = ConnectionPool.from_url(settings.REDIS_URL, max_connections=50, decode_responses=True)

class RedisClient:
    def __init__(self):
        self.client = Redis(connection_pool=pool)

    async def get(self, key: str) -> str | None:
        return await self.client.get(key)

    async def set(self, key: str, value: str, ttl: int = 3600) -> bool:
        return await self.client.set(name=key, value=value, ex=ttl)

    async def delete(self, key: str) -> int:
        return await self.client.delete(key)

redis_client = RedisClient()