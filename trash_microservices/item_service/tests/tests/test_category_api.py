from httpx import AsyncClient, Cookies
from loguru import logger
import pytest

from tests.tests.conftest import urls_dict, headers

@pytest.mark.asyncio(scope="module")
async def test_add_correct_category(client: AsyncClient, cookies: Cookies):
    category_dict_1 = {
        "name": "bricks",
    }

    re = await client.post(url=urls_dict["/categories/add/"],
                           headers=headers, json=category_dict_1)

    assert re.status_code == 200

    # cleanup
    await client.delete(url=urls_dict["/categories/add/"], headers=headers)

@pytest.mark.asyncio(scope="module")
async def test_add_incorrect_category_name(client: AsyncClient, cookies: Cookies):
    category_dict_1 = {
        "name": 123123,
    }

    re = await client.post(url=urls_dict["/categories/add/"],
                           headers=headers, json=category_dict_1)

    assert re.status_code == 200

    # cleanup
    await client.delete(url=urls_dict["/categories/add/"], headers=headers)


@pytest.mark.asyncio(scope="module")
async def test_add_correct_category(client: AsyncClient, cookies: Cookies):
    category_dict_1 = {
        "name": "bricks",
    }

    re = await client.post(url=urls_dict["/categories/add/"],
                           headers=headers, json=category_dict_1)

    assert re.status_code == 200

    # cleanup
    await client.delete(url=urls_dict["/categories/add/"], headers=headers)