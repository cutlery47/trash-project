from item_service.controller.exceptions import ResourceAccessDenied, AccessTokenInvalid, PermissionsDenied

from loguru import logger

from httpx import Response, AsyncClient

class RequestValidator:
    def __init__(self, urls: dict):
        self.urls = urls

    async def validate_access(self, cookies: dict):
        async with AsyncClient(cookies=cookies) as client:
            re = await client.post(url=self.urls['/validate_access/'])
            self._handle_access_denial(re)

    async def validate_access_to_id(self, user_id: int, cookies: dict):
        async with AsyncClient(cookies=cookies) as client:
            re = await client.post(url=self.urls['/validate_access/'] + str(user_id))
            self._handle_resource_denial(re)

    async def validate_admin(self, cookies: dict):
        async with AsyncClient(cookies=cookies) as client:
            re = await client.post(url=self.urls['/validate_admin/'])
            self._handle_id_denial(re)

    async def validate_access_and_admin(self, cookies: dict):
        async with AsyncClient(cookies=cookies) as client:
            re = await client.post(url=self.urls['/validate_access_and_admin/'])
            self._handle_access_denial(re)
            self._handle_id_denial(re)

    async def validate_access_and_id(self, user_id: int, cookies: dict):
        async with AsyncClient(cookies=cookies) as client:
            re = await client.post(url=self.urls['/validate_access_and_id/'] + str(user_id))
            self._handle_access_denial(re)
            self._handle_id_denial(re)

    @staticmethod
    def _handle_access_denial(re: Response):
        if re.status_code == 401:
            logger.error("Access token is invalid")
            raise AccessTokenInvalid()

    @staticmethod
    def _handle_resource_denial(re: Response):
        if re.status_code == 403:
            logger.error("You cannot access this resource")
            raise ResourceAccessDenied()

    @staticmethod
    def _handle_id_denial(re: Response):
        if re.status_code == 401:
            logger.error("You cannot access this resource")
            raise PermissionsDenied()
