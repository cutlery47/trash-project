from item_service.interfaces.base_repository import BaseRepository
from item_service.repositories.models.models import Item
from item_service.exceptions.repository_exceptions import (DataNotFoundException,
                                                           InternalRepositoryException, RepositoryException)

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.sql.expression import select
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy import delete, update

from loguru import logger


# noinspection PyTypeChecker
class ItemRepository(BaseRepository[Item]):
    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine

    async def create(self, item: Item) -> None:
        async with AsyncSession(self.engine) as session:
            try:
                session.add(item)
            except SQLAlchemyError as err:
                await session.rollback()
                logger.error(err.args[0])
                raise InternalRepositoryException("Couldn't create item")
            else:
                await session.commit()

    async def get(self, item_id: int) -> Item:
        async with AsyncSession(self.engine) as session:
            try:
                item = session.get_one(Item, item_id)
            except NoResultFound as exc:
                logger.error(exc.args[0])
                raise DataNotFoundException("Item not found")
            return item

    async def get_all(self) -> list[Item]:
        async with AsyncSession(self.engine) as session:
            statement = select(Item)
            items = (await session.execute(statement)).scalars().all()
            return items

    async def delete(self, item_id: int):
        async with AsyncSession(self.engine) as session:
            try:
                query = delete(Item).where(Item.id == item_id)
                await session.execute(query)
            except SQLAlchemyError as exc:
                await session.rollback()
                logger.error(exc.args[0])
                raise RepositoryException("Couldn't delete item")
            else:
                await session.commit()

    async def update(self, item_id: int, item: Item) -> Item:
        async with AsyncSession(self.engine) as session:
            try:
                # TODO: figure out how to get rid of implicit field declaration
                query = update(Item).where(Item.id == item_id).values(name=item.name,
                                                                      description=item.description,
                                                                      price=item.price,
                                                                      in_stock=item.in_stock,
                                                                      image=item.image)
                await session.execute(query)
            except SQLAlchemyError as exc:
                await session.rollback()
                logger.error(exc.args[0])
                raise RepositoryException("Couldn't update item")
            else:
                await session.commit()
