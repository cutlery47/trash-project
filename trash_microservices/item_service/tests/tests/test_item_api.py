import httpx

import json

from tests.tests.conftest import urls_path

from loguru import logger

email = "example_123@gmail.com"
password = "example_123_password"
user_id = ""
headers = {"Content-Type": "application/json"}
cookies = dict()
urls_dict = json.load(open(urls_path))

def test_register(client):
    global user_id

    re = httpx.post(url=urls_dict["/register/"], headers=headers,
                    json={"email": email, "password": password})
    user_id = re.text

    assert re.status_code == 200


def test_authorize(client):
    global cookies

    re = httpx.post(url=urls_dict["/authorize/"], headers=headers,
                    json={"email": email, "password": password})
    cookies = re.cookies

    assert re.status_code == 200


def test_add_correct_category(client):
    category_dict = {
        "name": "bricks",
    }

    re = client.post(url=urls_dict["/categories/add/"],
                     headers=headers, json=category_dict)

    assert re.status_code == 200


def test_add_incorrect_name_category(client):
    category_dict = {
        "name": 123,
    }

    re = client.post(url=urls_dict["/categories/add/"], headers=headers,
                     json=category_dict)

    assert re.status_code == 422


def test_add_correct_items(client):
    item_dict_1 = {
        "category_id": 1,
        "merchant_id": user_id,
        "name": "brick",
        "description": "brick!",
        "price": 10,
        "in_stock": 5,
    }

    item_dict_2 = {
        "category_id": 1,
        "merchant_id": user_id,
        "name": "Bogdan",
        "description": "Bogdan Shitov himself",
        "price": 228.1337,
        "in_stock": 2,
    }

    re_1 = client.post(url=urls_dict["/items/add/"], headers=headers,
                       json=item_dict_1, cookies=cookies)

    re_2 = client.post(url=urls_dict["/items/add/"], headers=headers,
                       json=item_dict_2, cookies=cookies)

    assert re_1.status_code == 200
    assert re_2.status_code == 200


def test_add_incorrect_item_category_id(client):
    item_dict_1 = {
        "category_id": -2,
        "merchant_id": user_id,
        "name": "skibidi",
        "description": "YES YES!",
        "price": 50,
        "in_stock": 100,
    }

    item_dict_2 = {
        "category_id": 1.5,
        "merchant_id": user_id,
        "name": "skibidi",
        "description": "YES YES!",
        "price": 50,
        "in_stock": 100,
    }

    re_1 = client.post(url=urls_dict["/items/add/"], headers=headers,
                       json=item_dict_1, cookies=cookies)

    re_2 = client.post(url=urls_dict["/items/add/"], headers=headers,
                       json=item_dict_2, cookies=cookies)

    assert re_1.status_code == 422
    assert re_2.status_code == 422


def test_add_incorrect_item_price(client):
    item_dict = {
        "category_id": 1,
        "merchant_id": user_id,
        "name": "skibidi",
        "description": "YES YES!",
        "price": -20.5,
        "in_stock": 100,
    }

    re = client.post(url=urls_dict["/items/add/"], headers=headers,
                     json=item_dict, cookies=cookies)

    assert re.status_code == 422


def test_add_incorrect_item_stock(client):
    item_dict = {
        "category_id": 1,
        "merchant_id": user_id,
        "name": "skibidi",
        "description": "YES YES!",
        "price": 20.5,
        "in_stock": -10,
    }

    re = client.post(url=urls_dict["/items/add/"], headers=headers,
                     json=item_dict, cookies=cookies)

    assert re.status_code == 422


def test_get_items(client):
    re = client.get(url=urls_dict["/items/"],
                    cookies=cookies)
    data = re.json()

    assert type(data) is list and len(data) == 2
    assert data[0]["name"] == "brick" and data[1]["name"] == "Bogdan"

def test_get_existing_item(client):
    re = client.get(url=urls_dict["/items/"] + "1",
                    cookies=cookies)
    data = re.json()

    assert type(data) is dict
    assert data["name"] == "brick"

def test_get_non_existing_item(client):
    re = client.get(url=urls_dict["/items/"] + "3",
                    cookies=cookies)

    assert re.status_code == 404


def test_unregister(client):
    re = httpx.delete(url=urls_dict["/users/delete/"] + user_id,
                      headers=headers, cookies=cookies)

    assert re.status_code == 200
