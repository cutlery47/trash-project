from item_service.interfaces.service import ServiceInterface
from item_service.interfaces.repository import RepositoryInterface

class Service(ServiceInterface):
    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    async def do_shi(self, data):
        return "XYU"
