from httpx import AsyncClient, Cookies
from loguru import logger
import pytest

from tests.tests.conftest import headers
from tests.tests.manager import RequestManager

from item_service.repositories.models.models import Item, Category

@pytest.mark.asyncio(scope="module")
async def test_add_correct_item(client: AsyncClient, user_id, cookies: Cookies) -> None:
    client.cookies = cookies
    client.headers = headers

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

    all_categories = await category_manager.get_all_serialized()
    category_id = all_categories[0]['id']
    item['category_id'] = category_id

    await item_manager.add(item)
    added_items = await item_manager.get_all_serialized()

    item_id = added_items[0]['id']

    assert added_items[0]["name"] == item['name']

    await category_manager.delete(category_id)
    await item_manager.delete(item_id)

@pytest.mark.asyncio(scope="module")
async def test_add_incorrect_item_merchant_id(client: AsyncClient, user_id, cookies):
    client.cookies = cookies
    client.headers = headers

    category_manager = RequestManager(client, Category)
    item_manager = RequestManager(client, Item)

    category = {"name": "bogdan"}

    item = {
        "merchant_id": 10,
        "name": "Bogdan",
        "description": "Bogdan Shitov himself",
        "price": 228.1337,
        "in_stock": 2,
    }

    await category_manager.add(category)
    added_categories = await category_manager.get_all_serialized()

    category_id = added_categories[0].get('id')
    item['category_id'] = category_id

    response = await item_manager.add(item)

    assert response.status_code != 200

@pytest.mark.asyncio(scope="module")
async def test_add_incorrect_item_category_id(client, user_id, cookies):
    client.cookies = cookies
    client.headers = headers

    item_manager = RequestManager(client, Item)

    item_1 = {
        "category_id": -2,
        "merchant_id": user_id,
        "name": "skibidi",
        "description": "YES YES!",
        "price": 50,
        "in_stock": 100,
    }

    item_2 = {
        "category_id": 1.5,
        "merchant_id": user_id,
        "name": "skibidi",
        "description": "YES YES!",
        "price": 50,
        "in_stock": 100,
    }

    re_1 = await item_manager.add(item_1)
    re_2 = await item_manager.add(item_2)

    assert re_1.status_code == 422
    assert re_2.status_code == 422

@pytest.mark.asyncio(scope="module")
async def test_add_incorrect_item_price(client, user_id, cookies):
    client.cookies = cookies
    client.headers = headers

    item_manager = RequestManager(client, Item)

    item = {
        "category_id": 1,
        "merchant_id": user_id,
        "name": "skibidi",
        "description": "YES YES!",
        "price": -20.5,
        "in_stock": 100,
    }

    response = await item_manager.add(item)

    assert response.status_code == 422

@pytest.mark.asyncio(scope="module")
async def test_add_incorrect_item_stock(client, user_id, cookies):
    client.cookies = cookies
    client.headers = headers

    category_manager = RequestManager(client, Category)
    item_manager = RequestManager(client, Item)

    category = {"name": "bogdan"}

    item_1 = {
        "category_id": 1,
        "merchant_id": user_id,
        "name": "skibidi",
        "description": "YES YES!",
        "price": 20.5,
        "in_stock": 10,
    }

    item_2 = {
        "category_id": 1,
        "merchant_id": user_id,
        "name": "skibadfasfidi",
        "description": "YES YES!",
        "price": 20.5,
        "in_stock": 10,
    }

    await category_manager.add(category)
    all_categories = await category_manager.get_all_serialized()
    cat_id = all_categories[0]['id']

    item_1['category_id'] = cat_id
    item_2['category_id'] = cat_id

    await item_manager.add(item_1)
    await item_manager.add(item_2)

    items = await item_manager.get_all_serialized()

    assert len(items) == 2

