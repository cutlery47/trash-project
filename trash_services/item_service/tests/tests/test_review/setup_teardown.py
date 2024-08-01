from httpx import AsyncClient, Cookies
from loguru import logger

from item_service.models.models import Item, Review, Category
from tests.tests.manager import RequestManager

async def setup(client: AsyncClient, user_id: int) -> (int, int):
    category_manager = RequestManager(client, Category)
    item_manager = RequestManager(client, Item)

    category = {"name": "bogdan"}

    item = {
        "merchant_id": user_id,
        "name": "brick",
        "description": "brick!",
        "price": 10,
        "in_stock": 5,
    }

    category_id = (await category_manager.add(category)).json()

    item['category_id'] = category_id
    item_id = (await item_manager.add(item)).json()

    return item_id, category_id


async def teardown(client: AsyncClient, item_id, category_id, review_ids: list[int]):
    category_manager = RequestManager(client, Category)
    item_manager = RequestManager(client, Item)
    review_manager = RequestManager(client, Review)

    for id_ in review_ids:
        await review_manager.delete(id_)
    await item_manager.delete(item_id)
    await category_manager.delete(category_id)


