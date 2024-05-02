from item_service.interfaces.service import ServiceInterface
from item_service.interfaces.controller import ControllerInterface

class Controller(ControllerInterface):
    def __init__(self, service: ServiceInterface):
        self.service = service

    def do_shi(self, data):
        return self.service.do_shi(data)
