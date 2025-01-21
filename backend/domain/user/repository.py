from abc import ABC, abstractmethod
from backend.domain.seedwork.repository import ICrudRepository
from backend.domain.user.entity import User


class IUserRepository(ICrudRepository[int, User], ABC):
    @abstractmethod
    def get_all(self) -> list[User]:
        raise NotImplementedError
