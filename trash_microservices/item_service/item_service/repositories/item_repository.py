from item_service.interfaces.base_repository import BaseRepository
from item_service.repositories.models.models import Item, UserItem

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

class ItemRepository(BaseRepository[Item]):
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    async def create(self, item: Item, user_item: UserItem) -> None:
        with Session(self.engine) as session:
            with session.begin():
                session.add(item)

    async def get(self, item_id: Item) -> Item | None:
        with Session(self.engine) as session:
            return session.get(Item, item_id)

    async def get_all(self) -> list[Item]:
        with Session(self.engine) as session:
            statement = select(Item)
            items = list(session.execute(statement).scalars().all())
            return items

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