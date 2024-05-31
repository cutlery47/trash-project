from item_service.cache.core.base_cache_client import BaseCacheClient

from pydantic import BaseModel

from redis.asyncio.client import Redis

from loguru import logger

class RedisClient(BaseCacheClient):

    def __init__(self, cache_backend: Redis):
        self._backend = cache_backend

    async def get(self, entity_class: str, entity_id: int) -> BaseModel | None:
        key = self._generate_key(entity_class, entity_id)
        data = await self._backend.hgetall(key)
        logger.info(f"Cached data: {data}. By key: {key}")

    async def delete(self, entity_class: str, entity_id: int) -> None:
        key = self._generate_key(entity_class, entity_id)
        res = await self._backend.delete(key)
        logger.info(f"Objects deleted from cache: {res}. By key: {key}")

    async def set(self, entity_class: str, entity: BaseModel) -> None:
        key = self._generate_key(entity_class, entity.id)
        res = await self._backend.hset(key, mapping=entity.model_dump())
        logger.info(f"Updated fields in hash: {res}. By key: {key}")

    async def ping(self):
        return await self._backend.ping()

    @staticmethod
    def _generate_key(entity_class: str, entity_id: int) -> str:
        return f"{entity_class}:{entity_id}"
