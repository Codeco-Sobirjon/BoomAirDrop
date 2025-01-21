from abc import ABC

from backend.domain.seedwork.repository import ICrudRepository
from .entity import GameStatus


class IGameRepository(ICrudRepository[int, GameStatus], ABC):
    pass
