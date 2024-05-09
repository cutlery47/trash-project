from item_service.interfaces.base_repository import BaseRepository
from item_service.repositories.models.models import Category
from item_service.exceptions.repository_exceptions import InternalRepositoryException

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from loguru import logger

class CategoryRepository(BaseRepository[Category]):
    def __init__(self, engine: Engine):
        self.engine = engine

    async def create(self, category: Category) -> None:
        with Session(self.engine) as session:
            session.begin()
            try:
                session.add(category)
            except SQLAlchemyError as err:
                logger.error(err.args[0])
                session.rollback()
                raise InternalRepositoryException("Couldn't create category")
            else:
                session.commit()

    async def get(self, category_id: Category) -> Category:
        pass

    async def get_all(self) -> list[Category]:
        pass

    async def update(self, category_id: int, category: Category) -> Category:
        pass

    async def delete(self, category_id: int):
        pass
