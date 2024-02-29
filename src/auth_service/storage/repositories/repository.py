from abc import ABC, abstractmethod


# an interface for other repos
class Repository[Entity](ABC):

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def get(self, id_: int) -> Entity:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Entity]:
        raise NotImplementedError

    @abstractmethod
    def add(self, data: Entity) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, id_: int, data: Entity) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id_: int) -> None:
        raise NotImplementedError



