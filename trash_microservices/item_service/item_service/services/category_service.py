from item_service.interfaces.base_service import BaseService
from item_service.interfaces.base_repository import BaseRepository
from item_service.schemas.category_schema import BaseCategory, Category, CategoryAdd


class CategoryService(BaseService[BaseCategory]):
    def __init__(self, repository: BaseRepository):
        self.repository = repository

    async def create(self, category: CategoryAdd) -> None:
        pass

    async def get(self, category_id: int) -> Category:
        pass

    async def get_all(self) -> list[Category]:
        pass

    async def update(self, category_id: int, item: CategoryAdd) -> None:
        pass

    async def delete(self, category_id: int) -> None:
        pass
