from item_service.cache.core.base_cache_manager import BaseCacheManager
from item_service.models.models import Base

from typing import Optional

from redis import Redis

import json

class RedisCacheManager(BaseCacheManager):

    def __init__(self, cache_backend: Redis):
        self._cache_backend = cache_backend

    def get(self, entity_class: str, entity_id: Optional[int] = None) -> Base | None:
        pass

    def delete(self, entity_class: str, entity_id: int) -> None:
        pass

    def set(self, entity_class: str, entity_id: int) -> None:
        pass

    @staticmethod
    def _generate_key(entity_class: str, entity_id: int) -> str:
        pass
