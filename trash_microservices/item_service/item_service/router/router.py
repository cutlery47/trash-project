from item_service.interfaces.router import RouterInterface
from item_service.interfaces.controller import ControllerInterface


class Router(RouterInterface):
    def __init__(self, controller: ControllerInterface):
        self.controller = controller

    def set_routes(self):
        pass



