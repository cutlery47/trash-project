from httpx import AsyncClient, Cookies
from loguru import logger
import pytest

from tests.tests.conftest import urls_dict, headers

@pytest.mark.asyncio(scope="module")
async def test_add_correct_category(client: AsyncClient, cookies: Cookies):
    client.cookies = cookies
    client.headers = headers

    category = {"name": "bricks"}

    # adding a new category
    await client.post(url=urls_dict["/categories/"], json=category)
    # retrieving the category
    re = await client.get(url=urls_dict["/categories/"] + "1")
    # checking if categories match
    assert re.json()[0].get("name") == category.get("name")
    # cleanup
    await client.delete(url=urls_dict["/categories/"] + "1")

@pytest.mark.asyncio(scope="module")
async def test_add_incorrect_category_name(client: AsyncClient, cookies: Cookies):
    client.cookies = cookies
    client.headers = headers

    category = {"name": 123123}

    # trying to add a fake category
    re = await client.post(url=urls_dict["/categories/"], headers=headers)
    # checking if request failed
    assert re.status_code == 422

@pytest.mark.asyncio(scope="module")
async def test_delete_existing_category(client: AsyncClient, cookies: Cookies):
    client.cookies = cookies
    client.headers = headers

    category = {"name": "bogdan"}

    # adding a new category
    await client.post(url=urls_dict["/categories/"], json=category)
    # deleting the category
    await client.delete(url=urls_dict["/categories/"] + "2")
    # trying to get the category
    re = await client.get(url=urls_dict["/categories/"] + "2")

    assert len(re.json()) == 0

@pytest.mark.asyncio(scope="module")
async def test_delete_nonexistent_category(client: AsyncClient, cookies: Cookies):
    # trying to delete a category
    re = await client.delete(url=urls_dict["/categories/"] + "1")

    assert re.status_code == 404

# @pytest.mark.asyncio(scope="module")
# async def test_update_category(client: AsyncClient, cookies: Cookies):
#     client.cookies = cookies
#     client.headers = headers
#
#     category = {"name": "buggin"}
#     new_category = {"name": "slaccin"}
#
#     await client.post(url=urls_dict["/categories/"], json=category)
#
#     await client.put(url=urls_dict["/categories/"] + "3", json=new_category)
#
#     re = await client.get(url=urls_dict["/categories/"] + "3")
#
#     assert re.json().get("name") == new_category.get("name")
#
#     await client.delete(url=urls_dict["/categories/"] + "3")
#
# @pytest.mark.asyncio(scope="module")
# async def test_update_category_incorrect_name(client: AsyncClient, cookies: Cookies):
#     category = {
#         "name": "buggin"
#     }
#
#     new_category = {
#         "name": 123123
#     }
#
#     await client.post(url=urls_dict["/categories/"],
#                       headers=headers,
#                       json=category,
#                       cookies=cookies)
#
#     re = await client.put(url=urls_dict["/categories/"] + "4",
#                           headers=headers,
#                           json=new_category,
#                           cookies=cookies)
#
#     assert re.status_code == 422
#
#     await client.delete(url=urls_dict["/categories/"] + "4",
#                         headers=headers,
#                         cookies=cookies)
#
# @pytest.mark.asyncio(scope="module")
# async def test_update_nonexistent_category(client: AsyncClient, cookies: Cookies):
#     category = {
#         "name": "buggin"
#     }
#
#     re = await client.put(url=urls_dict["/categories/"] + "228",
#                           headers=headers,
#                           json=category,
#                           cookies=cookies)
#
#     assert re.status_code == 404
# async def test_add_incorrect_category_name(client: AsyncClient, cookies: Cookies):
#     category = {
#         "name": 123123,
#     }
#
#     re = await client.post(url=urls_dict["/categories/"],
#                            headers=headers,
#                            json=category,
#                            cookies=cookies)
#
#     assert re.status_code == 422
#
# @pytest.mark.asyncio(scope="module")
# async def test_delete_existing_category(client: AsyncClient, cookies: Cookies):
#     category = {
#         "name": "bogdan"
#     }
#
#     re = await client.post(url=urls_dict["/categories/"],
#                            headers=headers,
#                            json=category,
#                            cookies=cookies)
#
#     re = await client.delete(url=urls_dict["/categories/"] + "2",
#                              headers=headers,
#                              cookies=cookies)
#
#     assert re.status_code == 200
#
# @pytest.mark.asyncio(scope="module")
# async def test_delete_nonexistent_category(client: AsyncClient, cookies: Cookies):
#     re = await client.delete(url=urls_dict["/categories/"] + "1",
#                              headers=headers,
#                              cookies=cookies)
#
#     assert re.status_code == 404
#
# @pytest.mark.asyncio(scope="module")
# async def test_update_category(client: AsyncClient, cookies: Cookies):
#     category = {
#         "name": "buggin"
#     }
#
#     new_category = {
#         "name": "slaccin"
#     }
#
#     await client.post(url=urls_dict["/categories/"],
#                       headers=headers,
#                       json=category,
#                       cookies=cookies)
#
#     await client.put(url=urls_dict["/categories/"] + "3",
#                      headers=headers,
#                      json=new_category,
#                      cookies=cookies)
#
#     re = await client.get(url=urls_dict["/categories/"] + "3",
#                           headers=headers,
#                           cookies=cookies)
#
#     assert re.json().get("name") == new_category.get("name")
#
#     await client.delete(url=urls_dict["/categories/"] + "3",
#                         headers=headers,
#                         cookies=cookies)
#
# @pytest.mark.asyncio(scope="module")
# async def test_update_category_incorrect_name(client: AsyncClient, cookies: Cookies):
#     category = {
#         "name": "buggin"
#     }
#
#     new_category = {
#         "name": 123123
#     }
#
#     await client.post(url=urls_dict["/categories/"],
#                       headers=headers,
#                       json=category,
#                       cookies=cookies)
#
#     re = await client.put(url=urls_dict["/categories/"] + "4",
#                           headers=headers,
#                           json=new_category,
#                           cookies=cookies)
#
#     assert re.status_code == 422
#
#     await client.delete(url=urls_dict["/categories/"] + "4",
#                         headers=headers,
#                         cookies=cookies)
#
# @pytest.mark.asyncio(scope="module")
# async def test_update_nonexistent_category(client: AsyncClient, cookies: Cookies):
#     category = {
#         "name": "buggin"
#     }
#
#     re = await client.put(url=urls_dict["/categories/"] + "228",
#                           headers=headers,
#                           json=category,
#                           cookies=cookies)
#
#     assert re.status_code == 404
