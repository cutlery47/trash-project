from httpx import AsyncClient, Cookies
import pytest

from tests.tests.conftest import headers
from tests.tests.manager import RequestManager
from item_service.repositories.models.models import Category

@pytest.mark.asyncio(scope="module")
async def test_add_correct_category(client: AsyncClient, user_id, cookies):
    client.cookies = cookies
    client.headers = headers

    manager = RequestManager(client, Category)

    category = {"name": "bricks"}

    await manager.add(category)
    added_categories = await manager.get_all_serialized()

    assert added_categories[0]["name"] == category["name"]

    await manager.delete(added_categories[0]['id'])

@pytest.mark.asyncio(scope="module")
async def test_add_incorrect_category_name(client: AsyncClient, user_id, cookies):
    client.cookies = cookies
    client.headers = headers

    manager = RequestManager(client, Category)

    category = {"name": 123123}

    response = await manager.add(category)
    assert response.status_code == 422

@pytest.mark.asyncio(scope="module")
async def test_delete_existing_category(client: AsyncClient, user_id, cookies: Cookies):
    client.cookies = cookies
    client.headers = headers

    manager = RequestManager(client, Category)

    category = {"name": "bogdan"}

    await manager.add(category)

    added_categories = await manager.get_all_serialized()
    id_ = added_categories[0].get('id')

    await manager.delete(id_)

    response = await manager.get(id_)
    assert len(response.json()) == 0

@pytest.mark.asyncio(scope="module")
async def test_delete_nonexistent_category(client: AsyncClient, user_id, cookies):
    client.cookies = cookies
    client.headers = headers

    manager = RequestManager(client, Category)

    response = await manager.delete(228)
    assert response.status_code == 404

@pytest.mark.asyncio(scope="module")
async def test_update_category(client: AsyncClient, user_id, cookies):
    client.cookies = cookies
    client.headers = headers

    manager = RequestManager(client, Category)

    category = {"name": "buggin"}
    new_category = {"name": "slaccin"}

    await manager.add(category)
    added_categories = await manager.get_all_serialized()

    id_ = added_categories[0].get('id')

    await manager.update(id_, new_category)
    response = await manager.get_serialized(id_)

    assert response.get("name") == new_category.get("name")

    await manager.delete(id_)

@pytest.mark.asyncio(scope="module")
async def test_update_category_incorrect_name(client: AsyncClient, user_id, cookies):
    client.cookies = cookies
    client.headers = headers

    manager = RequestManager(client, Category)

    category = {"name": "buggin"}
    new_category = {"name": 123123}

    await manager.add(category)

    added_categories = await manager.get_all_serialized()
    id_ = added_categories[0].get('id')

    response = await manager.update(id_, new_category)

    assert response.status_code == 422

    await manager.delete(id_)

@pytest.mark.asyncio(scope="module")
async def test_update_nonexistent_category(client: AsyncClient, user_id, cookies):
    client.cookies = cookies
    client.headers = headers

    manager = RequestManager(client, Category)

    category = {"name": "buggin"}

    response = await manager.update(1337, category)

    assert response.status_code == 404

