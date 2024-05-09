from item_service.interfaces.base_repository import BaseRepository
from item_service.repositories.models.models import Item
from item_service.exceptions.repository_exceptions import DataNotFoundException

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from sqlalchemy.exc import NoResultFound

from loguru import logger

class ItemRepository(BaseRepository[Item]):
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    async def create(self, item: Item) -> None:
        with Session(self.engine) as session:
            with session.begin():
                session.add(item)
                session.commit()

    # noinspection PyTypeChecker
    async def get(self, item_id: int) -> Item:
        with Session(self.engine) as session:
            try:
                item = session.get_one(Item, item_id)
            except NoResultFound as exc:
                logger.error(exc.args[0])
                raise DataNotFoundException("Item not found")
            return item

    async def get_all(self) -> list[Item]:
        with Session(self.engine) as session:
            statement = select(Item)
            items = list(session.execute(statement).scalars().all())
            return items

    async def update(self, item_id: int, item: Item) -> Item:
        pass

    async def delete(self, item_id: int):
        pass
