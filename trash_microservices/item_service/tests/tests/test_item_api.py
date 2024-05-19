from httpx import AsyncClient, Cookies
from loguru import logger
import pytest

from tests.tests.conftest import urls_dict, headers, user_id

@pytest.mark.asyncio(scope="module")
async def test_add_correct_items(client: AsyncClient, user_id: int, cookies: Cookies) -> None:
    category = {
        "name": "bogdan"
    }

    item = {
        "category_id": 1,
        "merchant_id": user_id,
        "name": "brick",
        "description": "brick!",
        "price": 10,
        "in_stock": 5,
    }

    await client.post(urls_dict["/categories/"],
                      headers=headers,
                      cookies=cookies,
                      json=item)

    await client.post(url=urls_dict["/items/"],
                      headers=headers,
                      json=item,
                      cookies=cookies)

    re = await client.get(url=urls_dict["/items/"] + "1",
                          headers=headers,
                          cookies=cookies)

    assert re.json().get("name") == item.get("name")

    await client.delete(urls_dict["/categories/"] + "1",
                        headers=headers,
                        cookies=cookies)

    await client.delete(url=urls_dict["/items/"] + "1",
                        headers=headers,
                        cookies=cookies)

# @pytest.mark.asyncio(scope="session")
# async def test_add_incorrect_item_merchant_id(client: AsyncClient, cookies: Cookies):
#     item_dict = {
#         "category_id": 1,
#         "merchant_id": 10,
#         "name": "Bogdan",
#         "description": "Bogdan Shitov himself",
#         "price": 228.1337,
#         "in_stock": 2,
#     }
#
#     re = await client.post(url=urls_dict["/items/add/"],
#                            headers=headers,
#                            json=item_dict,
#                            cookies=cookies)
#
#     assert re.status_code == 403
#
# @pytest.mark.asyncio(scope="session")
# async def test_add_incorrect_item_category_id(client):
#     item_dict_1 = {
#         "category_id": -2,
#         "merchant_id": user_id,
#         "name": "skibidi",
#         "description": "YES YES!",
#         "price": 50,
#         "in_stock": 100,
#     }
#
#     item_dict_2 = {
#         "category_id": 1.5,
#         "merchant_id": user_id,
#         "name": "skibidi",
#         "description": "YES YES!",
#         "price": 50,
#         "in_stock": 100,
#     }
#
#     re_1 = await client.post(url=urls_dict["/items/add/"], headers=headers,
#                              json=item_dict_1, cookies=cookies)
#
#     re_2 = await client.post(url=urls_dict["/items/add/"], headers=headers,
#                              json=item_dict_2, cookies=cookies)
#
#     assert re_1.status_code == 422
#     assert re_2.status_code == 422
#
# @pytest.mark.asyncio(scope="session")
# async def test_add_incorrect_item_price(client):
#     item_dict = {
#         "category_id": 1,
#         "merchant_id": user_id,
#         "name": "skibidi",
#         "description": "YES YES!",
#         "price": -20.5,
#         "in_stock": 100,
#     }
#
#     re = await client.post(url=urls_dict["/items/add/"], headers=headers,
#                            json=item_dict, cookies=cookies)
#
#     assert re.status_code == 422
#
# @pytest.mark.asyncio(scope="session")
# async def test_add_incorrect_item_stock(client):
#     item_dict = {
#         "category_id": 1,
#         "merchant_id": user_id,
#         "name": "skibidi",
#         "description": "YES YES!",
#         "price": 20.5,
#         "in_stock": -10,
#     }
#
#     re = await client.post(url=urls_dict["/items/add/"], headers=headers,
#                            json=item_dict, cookies=cookies)
#
#     assert re.status_code == 422
#
# @pytest.mark.asyncio(scope="session")
# async def test_get_items(client):
#     re = await client.get(url=urls_dict["/items/"],
#                           cookies=cookies)
#     data = re.json()
#
#     assert type(data) is list and len(data) == 2
#     assert data[0]["name"] == "brick" and data[1]["name"] == "Bogdan"
#
# @pytest.mark.asyncio(scope="session")
# async def test_get_existing_item(client):
#     re = await client.get(url=urls_dict["/items/"] + "1",
#                           cookies=cookies)
#     data = re.json()
#
#     assert type(data) is dict
#     assert data["name"] == "brick"
#
# @pytest.mark.asyncio(scope="session")
# async def test_get_non_existing_item(client):
#     re = await client.get(url=urls_dict["/items/"] + "3",
#                           cookies=cookies)
#
#     assert re.status_code == 404
#
# @pytest.mark.asyncio(scope="session")
# async def test_delete_own_item(client):
#     re = await client.delete(url=urls_dict["/items/"] + "1",
#                              cookies=cookies)
#
#     assert re.status_code == 200
#
# @pytest.mark.asyncio(scope="session")
# async def test_delete_non_existing_item(client):
#     re = await client.delete(url=urls_dict["/items/"] + "3",
#                              cookies=cookies)
#
#     assert re.status_code == 404
#
# @pytest.mark.asyncio(scope="session")
# async def test_update_existing_item(client):
#     updated_item_dict = {
#         "category_id": 1,
#         "merchant_id": user_id,
#         "name": "name",
#         "description": "brick!",
#         "price": 10.0,
#         "in_stock": 5,
#         "image": None
#     }
#
#     re_put = await client.put(url=urls_dict["/items/"] + "2",
#                               headers=headers,
#                               json=updated_item_dict,
#                               cookies=cookies)
#
#     assert re_put.status_code == 200
#
#     re_get = await client.get(url=urls_dict["/items/"] + "2",
#                               cookies=cookies)
#     re_get = re_get.json()
#     re_get.pop("id")
#
#     assert updated_item_dict == re_get
