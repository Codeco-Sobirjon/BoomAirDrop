from ..seedwork.repository import SqlAlchemyCrudRepository
from backend.domain.game.repository import IGameRepository
from backend.domain.game.entity import GameStatus
from .model import GameStatusModel


class GameRepository(IGameRepository, SqlAlchemyCrudRepository):
    model_class = GameStatusModel

    def delete(self, entity: GameStatus):
        raise NotImplementedError
