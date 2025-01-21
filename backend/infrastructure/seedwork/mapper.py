from abc import ABC, abstractmethod


class IObjectMapper[E, O](ABC):
    @abstractmethod
    def to_obj(self, obj: O) -> E:
        raise NotImplementedError

    @abstractmethod
    def from_obj(self, obj: E) -> O:
        raise NotImplementedError
