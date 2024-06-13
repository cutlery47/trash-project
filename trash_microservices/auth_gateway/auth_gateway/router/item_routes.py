from auth_gateway.router.router import Router

from flask import request, make_response

import httpx

def register_item_routes(router: Router):

    @router.get("/items/")
    def get_items():
        val = router.controller.validate_access()
        if val.status_code != 200:
            return val
        result = httpx.get(url="http://127.0.0.1:8000/api/v1/items/")
        return make_response(result.json(), result.status_code)

    @router.get("/items/<int:item_id>")
    def get_item(item_id):
        val = router.controller.validate_access()
        if val.status_code != 200:
            return val
        result = httpx.get(url="http://127.0.0.1:8000/api/v1/items/" + str(item_id))
        return make_response(result.json(), result.status_code)

    @router.post("/items/")
    def add_item():
        val = router.controller.validate_access()
        if val.status_code != 200:
            return val
        return httpx.post(url="http://127.0.0.1:8000/api/v1/items/",
                          json=request.json,
                          headers=request.headers,
                          cookies=request.cookies)

    @router.delete("/items/<int:item_id>")
    def delete_item(item_id):
        val = router.controller.validate_access()
        if val is not True:
            return val
        return httpx.delete(url="http://127.0.0.1:8000/api/v1/items/" + str(item_id),
                            headers=request.headers,
                            cookies=request.cookies)

    @router.put("/items/<int:item_id>")
    def update_item(item_id):
        val = router.controller.validate_access()
        if val is not True:
            return val
        return httpx.put(url="http://127.0.0.1:8000/api/v1/items/" + str(item_id),
                         json=request.json,
                         headers=request.headers)

