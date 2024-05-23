from tests.tests.conftest import urls_dict
from httpx import AsyncClient, Response

from loguru import logger

from item_service.repositories.models.models import Base, Category, Review, Item

class RequestManager:

    def __init__(self, client: AsyncClient, entity_class: type(Base)):
        self.client = client
        self.entity_class = entity_class
        self.url = self._get_url()

    async def add(self, data: dict) -> Response:
        response = await self.client.post(url=self.url, json=data)
        return response

    async def get(self, id_: int) -> Response:
        response = await self.client.get(url=self.url + str(id_))
        return response

    async def get_serialized(self, id_: int) -> dict:
        category = await self.get(id_)
        return category.json()[0]

    async def get_all(self) -> Response:
        response = await self.client.get(url=self.url)
        return response

    async def get_all_serialized(self) -> list[dict]:
        categories = await self.get_all()
        return categories.json()

    async def delete(self, id_: int,) -> Response:
        response = await self.client.delete(url=self.url + str(id_))
        return response

    async def update(self, id_: int, data: dict) -> Response:
        response = await self.client.put(url=self.url + str(id_), json=data)
        return response

    def _get_url(self):
        if self.entity_class == Category:
            return urls_dict["/categories/"]
        elif self.entity_class == Item:
            return urls_dict["/items/"]
        elif self.entity_class == Review:
            return urls_dict["/reviews/"]
