from item_service.cache.core.base_cache_client_factory import BaseCacheClientFactory

from item_service.cache.redis_client import RedisClient

from aioredis import Redis
from aioredis.connection import ConnectionPool

class RedisClientFactory(BaseCacheClientFactory[RedisClient]):

    def __init__(self, connection_pool: ConnectionPool):
        self._connection_pool = connection_pool

    def create(self) -> RedisClient:
        redis = Redis(connection_pool=self._connection_pool)
        return RedisClient(cache_backend=redis)
