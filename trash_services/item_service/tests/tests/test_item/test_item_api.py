from httpx import AsyncClient, Cookies
from loguru import logger
import pytest

from tests.tests.conftest import headers
from tests.tests.manager import RequestManager

from item_service.models.models import Item, Category

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

    category_res = await category_manager.add(category)
    category_id = category_res.json()
    item['category_id'] = category_id

    item_res = await item_manager.add(item)
    item_id = item_res.json()
    added_items = await item_manager.get_all_serialized()

    assert added_items[0]["name"] == item['name']

    await item_manager.delete(item_id)
    await category_manager.delete(category_id)


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

    category_res = await category_manager.add(category)
    category_id = category_res.json()

    item['category_id'] = category_id

    response = await item_manager.add(item)

    assert response.status_code != 200

    await category_manager.delete(category_id)

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

    category_res = await category_manager.add(category)
    category_id = category_res.json()

    item_1['category_id'] = category_id
    item_2['category_id'] = category_id

    item_1_id = (await item_manager.add(item_1)).json()
    item_2_id = (await item_manager.add(item_2)).json()

    items = await item_manager.get_all_serialized()

    assert len(items) == 2

    await item_manager.delete(item_1_id)
    await item_manager.delete(item_2_id)
    await category_manager.delete(category_id)

