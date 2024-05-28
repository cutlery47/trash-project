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

    await category_manager.add(category)
    await item_manager.add(item)

    items = await item_manager.get_all_serialized()
    categories = await category_manager.get_all_serialized()

    return items[0]['id'], categories[0]['id']


async def teardown(client: AsyncClient, item_id, category_id, review_ids: list[int]):
    category_manager = RequestManager(client, Category)
    item_manager = RequestManager(client, Item)
    review_manager = RequestManager(client, Review)

    await category_manager.delete(category_id)
    await item_manager.delete(item_id)
    for id_ in review_ids:
        await review_manager.delete(id_)
