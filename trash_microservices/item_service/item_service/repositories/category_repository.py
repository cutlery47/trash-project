from item_service.interfaces.repository import RepositoryInterface
from item_service.repositories.models.models import Category

from sqlalchemy.engine import Engine

class CategoryRepository(RepositoryInterface[Category]):
    def __init__(self, engine: Engine):
        self.engine = engine

    async def create(self, category: Category) -> Category:
        pass

    async def get(self, category_id: Category) -> Category:
        pass

    async def get_all(self) -> list[Category]:
        pass

    async def update(self, category_id: int, category: Category) -> Category:
        pass

    async def delete(self, category_id: int):
        pass
