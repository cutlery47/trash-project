from item_service.cache.core.base_cache_client_factory import BaseCacheClientFactory

from item_service.cache.redis_client import RedisClient

from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool

class RedisClientFactory(BaseCacheClientFactory):
    _self = None
    _connection_pool = None

    def __new__(cls, connection_pool: ConnectionPool):
        if not isinstance(cls._self, cls):
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self, connection_pool: ConnectionPool):
        self._connection_pool = connection_pool

    @classmethod
    def create(cls) -> RedisClient:
        redis = Redis(connection_pool=cls._connection_pool, decode_responses=True)
        return RedisClient(cache_backend=redis)
