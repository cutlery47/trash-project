from abc import ABC, abstractmethod

from item_service.storage.models import UserItem, Item

class RepositoryInterface:
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    async def add_item(self, item: Item, user_item: UserItem) -> None:
        raise NotImplementedError
