from item_service.interfaces.base_repository import BaseRepository
from item_service.repositories.models.models import Category
from item_service.exceptions.repository_exceptions import InternalRepositoryException, DataNotFoundException

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy import select, update, delete

from loguru import logger

class CategoryRepository(BaseRepository[Category]):
    def __init__(self, engine: AsyncEngine, sessionmaker: async_sessionmaker[AsyncSession]):
        self.engine = engine
        self.sessionmaker = sessionmaker

    async def create(self, category: Category) -> None:
        async with self.sessionmaker() as session:
            try:
                session.add(category)
            except SQLAlchemyError as err:
                await session.rollback()
                logger.error(err.args[0])
                raise InternalRepositoryException("Couldn't create category")
            else:
                await session.commit()

    async def get(self, category_id: Category) -> Category:
        async with self.sessionmaker() as session:
            try:
                category = await session.get_one(entity=Category, ident=category_id)
            except NoResultFound as err:
                logger.error(err.args[0])
                raise DataNotFoundException("Category not found")
            except SQLAlchemyError as err:
                logger.error(err.args[0])
                raise InternalRepositoryException("Couldn't get category")
            return category

    async def get_all(self) -> list[Category]:
        async with self.sessionmaker() as session:
            try:
                query = select(Category)
                categories_future = await session.execute(query)
                categories = categories_future.scalars().all()
            except SQLAlchemyError as err:
                logger.error(err.args[0])
                raise InternalRepositoryException("Couldn't get categories")
            return categories

    async def update(self, category_id: int, category: Category) -> None:
        async with self.sessionmaker() as session:
            try:
                query = update(Category).where(Category.id == category_id).values(name=category.name)
                await session.execute(query)
            except SQLAlchemyError as err:
                await session.rollback()
                logger.error(err.args[0])
                raise InternalRepositoryException("Couldn't update category")
            else:
                await session.commit()

    async def delete(self, category_id: int):
        async with self.sessionmaker() as session:
            try:
                query = delete(Category).where(Category.id == category_id)
                await session.execute(query)
            except SQLAlchemyError as err:
                await session.rollback()
                logger.error(err.args[0])
                raise InternalRepositoryException("Couldn't delete category")
            else:
                await session.commit()
