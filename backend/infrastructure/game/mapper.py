from abc import ABC

from backend.domain.game.entity import GameStatus
from .model import GameStatusModel
from ..seedwork.mapper import IObjectMapper


class GameStatusModelMapper(IObjectMapper[GameStatus, GameStatusModel]):

    def to_obj(self, obj: GameStatusModel) -> GameStatus:
        return GameStatus(
            id=1, total_users=obj.total_users, total_balance=obj.total_balance
        )

    def from_obj(self, obj: GameStatus) -> GameStatusModel:
        return GameStatusModel(
            id=1, total_users=obj.total_users, total_balance=obj.total_balance
        )
