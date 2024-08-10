import os

import aiohttp

from fastapi import Request

from src.router.router import Router


ITEM_SERVICE_HOST = os.getenv("ITEM_SERVICE_HOST", "localhost")
ITEM_SERVICE_PORT = os.getenv("ITEM_SERVICE_PORT", "9876")

def register_item_routes(router: Router):

    # === ITEMS ===

    @router.api.get("/items/")
    async def get_items(request: Request):
        router.controller.validate_access_token(request)

        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"http://{ITEM_SERVICE_HOST}:{ITEM_SERVICE_PORT}/api/v1/items/",
                                   headers=request.headers
                                   ) as response:
                return await response.json()

    @router.api.get("/items/{item_id}")
    async def get_item(request: Request, item_id: int):
        router.controller.validate_access_token(request)

        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"http://{ITEM_SERVICE_HOST}:{ITEM_SERVICE_PORT}/api/v1/items/{str(item_id)}",
                                   headers=request.headers) as response:
                return await response.json()

    @router.api.post("/items/")
    async def add_item(request: Request):
        router.controller.validate_access_token(request)

        async with aiohttp.ClientSession() as session:
            async with session.post(url=f"http://{ITEM_SERVICE_HOST}:{ITEM_SERVICE_PORT}/api/v1/items/",
                                    headers=request.headers,
                                    body=await request.body()) as response:
                return await response.json()

    @router.api.delete("/items/{item_id}")
    async def delete_item(request: Request, item_id: int):
        router.controller.validate_access_token(request)

        async with aiohttp.ClientSession() as session:
            async with session.delete(url=f"http://{ITEM_SERVICE_HOST}:{ITEM_SERVICE_PORT}/api/v1/items/{str(item_id)}",
                                      headers=request.headers) as response:
                return await response.json()

    @router.api.put("/items/{item_id}")
    async def update_item(request: Request, item_id: int):
        router.controller.validate_access_token(request)

        async with aiohttp.ClientSession() as session:
            async with session.put(url=f"http://{ITEM_SERVICE_HOST}:{ITEM_SERVICE_PORT}/api/v1/items/{str(item_id)}",
                                   headers=request.headers,
                                   body=await request.body()) as response:
                return await response.json()

    # === CATEGORIES ===

    @router.api.get("/categories/")
    async def get_categories(request: Request):
        router.controller.validate_access_token(request)

        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"http://{ITEM_SERVICE_HOST}:{ITEM_SERVICE_PORT}/api/v1/categories/",
                                   headers=request.headers) as response:
                return await response.json()

    @router.api.get("/categories/{category_id}")
    async def get_category(request: Request, category_id: int):
        router.controller.validate_access_token(request)

        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"http://{ITEM_SERVICE_HOST}:{ITEM_SERVICE_PORT}/api/v1/categories/{str(category_id)}",
                                   headers=request.headers) as response:
                return await response.json()

    @router.api.post("/categories/")
    async def add_category(request: Request):
        router.controller.validate_access_token(request)

        async with aiohttp.ClientSession() as session:
            async with session.post(url=f"http://{ITEM_SERVICE_HOST}:{ITEM_SERVICE_PORT}/api/v1/categories/",
                                    headers=request.headers,
                                    body=await request.body()) as response:
                return await response.json()

    @router.api.delete("/categories/{category_id}")
    async def delete_category(request: Request, category_id: int):
        router.controller.validate_access_token(request)

        async with aiohttp.ClientSession() as session:
            async with session.post(url=f"http://{ITEM_SERVICE_HOST}:{ITEM_SERVICE_PORT}/api/v1/categories/{str(category_id)}",
                                    headers=request.headers) as response:
                return await response.json()

    @router.api.put("/categories/{category_id}")
    async def delete_category(request: Request, category_id: int):
        router.controller.validate_access_token(request)

        async with aiohttp.ClientSession() as session:
            async with session.post(url=f"http://{ITEM_SERVICE_HOST}:{ITEM_SERVICE_PORT}/api/v1/categories/{str(category_id)}",
                                    headers=request.headers,
                                    body=await request.body()) as response:
                return await response.json()

    # === REVIEWS ===

    @router.api.get("/reviews/")
    async def get_categories(request: Request):
        router.controller.validate_access_token(request)

        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"http://{ITEM_SERVICE_HOST}:{ITEM_SERVICE_PORT}/api/v1/reviews/",
                                   headers=request.headers) as response:
                return await response.json()

    @router.api.get("/reviews/{review_id}")
    async def get_category(request: Request, review_id: int):
        router.controller.validate_access_token(request)

        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"http://{ITEM_SERVICE_HOST}:{ITEM_SERVICE_PORT}/api/v1/reviews/{str(review_id)}",
                                   headers=request.headers) as response:
                return await response.json()

    @router.api.post("/reviews/")
    async def add_category(request: Request):
        router.controller.validate_access_token(request)

        async with aiohttp.ClientSession() as session:
            async with session.post(url=f"http://{ITEM_SERVICE_HOST}:{ITEM_SERVICE_PORT}/api/v1/reviews/",
                                    headers=request.headers,
                                    body=await request.body()) as response:
                return await response.json()

    @router.api.delete("/reviews/{review_id}")
    async def delete_category(request: Request, review_id: int):
        router.controller.validate_access_token(request)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=f"http://{ITEM_SERVICE_HOST}:{ITEM_SERVICE_PORT}/api/v1/reviews/{str(review_id)}",
                    headers=request.headers) as response:
                return await response.json()

    @router.api.put("/reviews/{review_id}")
    async def delete_category(request: Request, review_id: int):
        router.controller.validate_access_token(request)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                    url=f"http://{ITEM_SERVICE_HOST}:{ITEM_SERVICE_PORT}/api/v1/reviews/{str(review_id)}",
                    headers=request.headers,
                    body=await request.body()) as response:
                return await response.json()
