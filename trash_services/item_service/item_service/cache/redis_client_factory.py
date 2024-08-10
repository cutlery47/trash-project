from item_service.cache.core.base_cache_client_factory import BaseCacheClientFactory
from item_service.config.cache.cache_config import CacheConfig
from item_service.cache.redis_client import RedisClient

from redis.asyncio.client import Redis
from redis.connection import ConnectionPool

from dataclasses import asdict

class RedisClientFactory(BaseCacheClientFactory):
    _self = None
    _config = None

    def __new__(cls, config: CacheConfig):
        if not isinstance(cls._self, cls):
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self, config: CacheConfig):
        self.config = config

    @classmethod
    def create(cls) -> RedisClient:
        connection_pool = ConnectionPool(**asdict(cls._config))
        redis = Redis(connection_pool=connection_pool, decode_responses=True)
        return RedisClient(cache_backend=redis)
