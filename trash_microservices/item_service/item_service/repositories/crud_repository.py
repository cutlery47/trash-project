from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import select, update, delete

from loguru import logger

from item_service.interfaces.base_repository import BaseRepository
from item_service.repositories.models.models import Base
from item_service.repositories.handlers.exception_handler import RepositoryExceptionHandler

from fastapi import Depends

from typing import Annotated

class CRUDRepository[Entity: Base](BaseRepository):
    def __init__(self,
                 engine: Annotated[AsyncEngine, Depends(get_engine)],
                 sessionmaker: Annotated[type(AsyncSession), Depends(get_sessionmaker)],
                 exc_handler: Annotated[RepositoryExceptionHandler, Depends(get_repo_excpetion_handler)]
                 ):
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

    async def get(self, **filters) -> list[Entity]:
        async with self.sessionmaker() as session:
            try:
                query = select(Entity).where(**filters)
                future = await session.execute(query)
            except (NoResultFound, SQLAlchemyError) as exc:
                self.exc_handler.handle(exc)
            else:
                data = list(future.scalars().all())
                return data

    async def delete(self, **filters) -> None:
        async with self.sessionmaker() as session:
            try:
                query = delete(Entity).where(**filters)
                await session.execute(query)
            except SQLAlchemyError as exc:
                await session.rollback()
                self.exc_handler.handle(exc)
            else:
                await session.commit()

    async def update(self, entity: Entity, **filters) -> None:
        async with self.sessionmaker() as session:
            try:
                query = update(Entity).where(**filters)
                await session.execute(query)
            except SQLAlchemyError as exc:
                await session.rollback()
                self.exc_handler.handle(exc)
            else:
                await session.commit()


