from fastapi import APIRouter

from item_service.interfaces.service import ServiceInterface
from item_service.interfaces.controller import ControllerInterface

class Controller(ControllerInterface):

    def __init__(self, service: ServiceInterface):
        self.service = service

    def setup_api(self) -> None:
        pass

    def get_api(self) -> APIRouter:
        pass
