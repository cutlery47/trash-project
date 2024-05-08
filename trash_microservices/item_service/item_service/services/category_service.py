from item_service.interfaces.base_service import BaseService
from item_service.schemas.category_schema import BaseCategoryDTO, CategoryDTO, CategoryAddDTO
from item_service.repositories.category_repository import CategoryRepository
from item_service.repositories.models.models import Category


class CategoryService(BaseService[BaseCategoryDTO]):
    def __init__(self, repository: CategoryRepository) -> None:
        self.repository = repository

    async def create(self, category: CategoryAddDTO) -> None:
        orm_category = Category(**category.dict())
        await self.repository.create(orm_category)

    async def get(self, category_id: int) -> CategoryDTO:
        pass

    async def get_all(self) -> list[CategoryDTO]:
        pass

    async def update(self, category_id: int, item: CategoryAddDTO) -> None:
        pass

    async def delete(self, category_id: int) -> None:
        pass
