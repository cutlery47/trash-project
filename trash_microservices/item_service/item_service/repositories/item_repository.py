from item_service.interfaces.base_repository import BaseRepository
from item_service.repositories.models.models import Item, UserItem

from sqlalchemy.engine import Engine

class ItemRepository(BaseRepository[Item]):
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    async def create(self, item: Item) -> Item:
        pass

    async def get(self, item_id: Item) -> Item:
        pass

    async def get_all(self) -> list[Item]:
        return ["123123123"]

    async def update(self, item_id: int, item: Item) -> Item:
        pass

    async def delete(self, item_id: int):
        pass

    #
    #
    # async def add_item(self, item: Item, user_item: UserItem):
    #     with Session(self.engine) as session:
    #         session.add(item)
    #         session.add(user_item)
    #         session.commit()