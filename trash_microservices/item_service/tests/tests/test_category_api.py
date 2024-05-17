from httpx import AsyncClient, Cookies
from loguru import logger
import pytest

from tests.tests.conftest import urls_dict, headers

@pytest.mark.asyncio(scope="module")
async def test_add_correct_category(client: AsyncClient, cookies: Cookies):
    category = {
        "name": "bricks",
    }

    re = await client.post(url=urls_dict["/categories/"], headers=headers,
                           json=category, cookies=cookies)

    assert re.status_code == 200

    # cleanup
    await client.delete(url=urls_dict["/categories/"],
                        headers=headers, cookies=cookies)

@pytest.mark.asyncio(scope="module")
async def test_add_incorrect_category_name(client: AsyncClient, cookies: Cookies):
    category = {
        "name": 123123,
    }

    re = await client.post(url=urls_dict["/categories/"],
                           headers=headers, json=category)

    assert re.status_code == 422

    # cleanup
    await client.delete(url=urls_dict["/categories/"],
                        headers=headers, cookies=cookies)

@pytest.mark.asyncio(scope="module")
async def test_delete_existing_category(client: AsyncClient, cookies: Cookies):
    category = {
        "name": "bogdan"
    }

    await client.post(url=urls_dict["/categories/"], headers=headers,
                      json=category, cookies=cookies)

    re = await client.delete(url=urls_dict["/categories/"] + "1",
                             headers=headers, cookies=cookies)

    assert re.status_code == 200

@pytest.mark.asyncio(scope="module")
async def test_delete_nonexistent_category(client: AsyncClient, cookies: Cookies):
    re = await client.delete(url=urls_dict["/categories/"] + "1",
                             headers=headers, cookies=cookies)

    assert re.status_code == 404

@pytest.mark.asyncio(scope="module")
async def test_update_category(client: AsyncClient, cookies: Cookies):
    category = {
        "name": "buggin"
    }

    new_category = {
        "name": "slaccin"
    }

    await client.post(url=urls_dict["/categories/"], headers=headers,
                      json=category, cookies=cookies)

    re = await client.put(url=urls_dict["/categories/"] + "1", headers=headers,
                          json=new_category, cookies=cookies)

    assert re.status_code == 200

    await client.delete(url=urls_dict["/categories/"] + "1",
                        headers=headers, cookies=cookies)




