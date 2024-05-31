from abc import ABC, abstractmethod

from pydantic import BaseModel

from item_service.schemas.schemas.review_schema import ReviewDTO

class BaseService[DTO: BaseModel](ABC):

    @abstractmethod
    async def create(self, dto: DTO) -> int:
        """
        Carries out business logic to create a new entity.
        :param dto:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def get(self, dto_id: int) -> list[DTO]:
        """
        Carries out business logic to get a specific entity.
        :param dto_id:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, dto_id: int, dto: DTO) -> None:
        """
        Carries out business logic to update a specific entity.
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, dto_id: int) -> None:
        """
        Carries out business logic to delete a specific entity.
        :param dto_id:
        :return:
        """
        raise NotImplementedError

class BaseReviewService(BaseService):

    @abstractmethod
    async def get_by_item_id(self, item_id: int) -> list[ReviewDTO]:
        """
        Carries out business logic to get all the Reviews for a specific item
        :param item_id:
        :return:
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> list[ReviewDTO]:
        """
        Carries out business logic to get all the Reviews for a specific user
        :param user_id:
        :return:
        """
        raise NotImplementedError
