from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, delete

from src.repositories.core.base_repository import BaseRepository
from src.models.models import Base
from src.repositories.exceptions import DataNotFoundException
from src.repositories.handlers.exception_handler import RepositoryExceptionHandler


class CRUDRepository[Entity: Base](BaseRepository):
    _entity_class = Base

    def __init__(self,
                 engine: AsyncEngine,
                 sessionmaker: async_sessionmaker[AsyncSession],
                 exc_handler: RepositoryExceptionHandler):
        self.engine = engine
        self.sessionmaker = sessionmaker
        self.exc_handler = exc_handler

    async def create(self, entity: Entity) -> None:
        async with self.sessionmaker() as session:
            try:
                session.add(entity)
            except SQLAlchemyError as exc:
                await session.rollback()
                self.exc_handler.handle(exc)
            else:
                await session.commit()

    async def get(self, *filters) -> list[Entity]:
        async with self.sessionmaker() as session:
            try:
                query = select(self._entity_class).where(*filters)
                future = await session.execute(query)
            except SQLAlchemyError as exc:
                self.exc_handler.handle(exc)
            else:
                data = list(future.scalars().all())
                return data

    async def delete(self, *filters) -> None:
        async with self.sessionmaker() as session:
            try:
                query = delete(self._entity_class).where(*filters)
                future = await session.execute(query)
                if future.rowcount == 0:
                    raise DataNotFoundException
            except SQLAlchemyError as exc:
                await session.rollback()
                self.exc_handler.handle(exc)
            else:
                await session.commit()

    async def update(self, entity: Entity, *filters) -> None:
        async with self.sessionmaker() as session:
            try:
                dict_entity = entity.serialize()
                query = update(self._entity_class).where(*filters).values(dict_entity)
                future = await session.execute(query)
                if future.rowcount == 0:
                    raise DataNotFoundException
            except SQLAlchemyError as exc:
                await session.rollback()
                self.exc_handler.handle(exc)
            else:
                await session.commit()


