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
    def create(self, entity_data: Entity) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update(self, id_: int, data: Entity) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id_: int) -> bool:
        raise NotImplementedError
