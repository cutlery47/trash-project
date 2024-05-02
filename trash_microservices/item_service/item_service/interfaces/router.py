from abc import ABC, abstractmethod

from item_service.interfaces.controller import ControllerInterface

from fastapi import APIRouter


class RouterInterface(ABC):

    @abstractmethod
    def __init__(self, controller: ControllerInterface) -> None:
        raise NotImplementedError

    # each of these two functions execute exactly once.
    # this made me assume that I CAN afford to make them sync.
    # idk, I jus feel like them being async doesn't make much sense,
    # as it will very barely affect application performance
    # --- MAYBE IM WRONG IDK---

    @abstractmethod
    def setup_api(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_api(self) -> APIRouter:
        raise NotImplementedError

