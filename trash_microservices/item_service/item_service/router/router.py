from django.urls import path

class Router:
    def __init__(self, controller):
        self.controller = controller
        self.routes = self.set_routes()

    def set_routes(self):
        return [
            path("", self.controller.home),
            path("add/", self.controller.add)
        ]

