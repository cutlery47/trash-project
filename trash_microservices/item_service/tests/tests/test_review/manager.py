from tests.tests.manager import RequestManager
from tests.tests.conftest import urls_dict
from httpx import Response


class ReviewRequestManager(RequestManager):

    async def get_by_item_id(self, item_id: int) -> Response:
        response = await self.client.get(urls_dict['/reviews/'] + "items/" + str(item_id))
        return response

    async def get_by_item_id_serialized(self, item_id: int) -> list[dict]:
        data = await self.get_by_item_id(item_id)
        return data.json()

    async def get_by_user_id(self, user_id: int) -> Response:
        response = await self.client.get(urls_dict['/reviews/'] + "users/" + str(user_id))
        return response

    async def get_by_user_id_serialized(self, user_id: int) -> list[dict]:
        data = await self.get_by_user_id(user_id)
        return data.json()

