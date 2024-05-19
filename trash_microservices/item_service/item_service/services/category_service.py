from item_service.interfaces.base_service import BaseService
from item_service.schemas.category_schema import BaseCategoryDTO, CategoryDTO, CategoryAddDTO
from item_service.interfaces.base_repository import BaseRepository
from item_service.repositories.models.models import Category


class CategoryService(BaseService[BaseCategoryDTO]):
    def __init__(self, repository: BaseRepository[Category]) -> None:
        self.repository = repository

    async def create(self, category: CategoryAddDTO) -> None:
        orm_category = Category(**category.model_dump())
        await self.repository.create(orm_category)

    async def get(self, category_id: int) -> CategoryDTO:
        orm_category = await self.repository.get(category_id)
        return CategoryDTO.model_validate(orm_category, from_attributes=True)

    async def get_all(self) -> list[CategoryDTO]:
        orm_categories = await self.repository.get_all()
        return [CategoryDTO.model_validate(orm_category, from_attributes=True) for orm_category in orm_categories]

    async def update(self, category_id: int, category: CategoryAddDTO) -> None:
        orm_category = Category(**category.model_dump())
        await self.repository.update(category_id, orm_category)

    async def delete(self, category_id: int) -> None:
        await self.repository.delete(category_id)
