from abc import ABC, abstractmethod
from .entity import Entity


class ICrudRepository[ID, E: Entity](ABC):
    @abstractmethod
    def get_by_id(self, id: ID) -> E | None:
        raise NotImplementedError

    @abstractmethod
    def create(self, entity: E):
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity: E):
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: E):
        raise NotImplementedError
