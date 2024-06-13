from item_service.cache.core.base_cache_client import BaseCacheClient

from pydantic import BaseModel

from redis.asyncio.client import Redis

from loguru import logger

class RedisClient(BaseCacheClient):

    def __init__(self, cache_backend: Redis):
        self._backend = cache_backend

    async def get(self, name: str, id_: int) -> dict | None:
        key = self._generate_key(name, id_)
        data = await self._backend.hgetall(key)

        logger.info(f"Cached data: {data}. By key: {key}")
        return data

    async def delete(self, name: str, id_: int) -> None:
        key = self._generate_key(name, id_)
        res = await self._backend.delete(key)

        logger.info(f"Objects deleted from cache: {res}. By key: {key}")

    async def set(self, name: str, data: dict, id_: int) -> None:
        key = self._generate_key(name, id_)
        res = await self._backend.hset(key, mapping=data)

        logger.info(f"Updated fields in hash: {res}. By key: {key}")

    @staticmethod
    def _generate_key(name: str, id_: int) -> str:
        return f"{name}:{id_}"
