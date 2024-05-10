from item_service.interfaces.base_repository import BaseRepository
from item_service.repositories.models.models import Item
from item_service.exceptions.repository_exceptions import (DataNotFoundException,
                                                           InternalRepositoryException, RepositoryException)

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy import delete, update

from loguru import logger


# noinspection PyTypeChecker
class ItemRepository(BaseRepository[Item]):
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    async def create(self, item: Item) -> None:
        with Session(self.engine) as session:
            session.begin()
            try:
                session.add(item)
            except SQLAlchemyError as err:
                session.rollback()
                logger.error(err.args[0])
                raise InternalRepositoryException("Couldn't create item")
            else:
                session.commit()

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

    async def delete(self, item_id: int):
        with Session(self.engine) as session:
            try:
                query = delete(Item).where(Item.id == item_id)
                session.execute(query)
            except SQLAlchemyError as exc:
                session.rollback()
                logger.error(exc.args[0])
                raise RepositoryException("Couldn't delete item")
            else:
                session.commit()

    async def update(self, item_id: int, item: Item) -> Item:
        with Session(self.engine) as session:
            try:
                # TODO: figure out how to optimize this
                query = update(Item).where(Item.id == item_id).values(name=item.name,
                                                                      description=item.description,
                                                                      price=item.price,
                                                                      in_stock=item.in_stock,
                                                                      image=item.image)
                session.execute(query)
            except SQLAlchemyError as exc:
                session.rollback()
                logger.error(exc.args[0])
                raise RepositoryException("Couldn't update item")
            else:
                session.commit()
