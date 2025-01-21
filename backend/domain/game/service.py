from backend.domain.game.entity import GameStatus
from .repository import IGameRepository


class GameService:
    def __init__(self, repository: IGameRepository):
        self.__repository = repository

    def get_game_status(self) -> GameStatus:
        res = self.__repository.get_by_id(GameStatus.id)
        assert res is not None
        return res

    def increase_user_count(self):
        res = self.__repository.get_by_id(GameStatus.id)
        assert res is not None
        res.total_users += 1
        self.__repository.update(res)
        return res

    def increase_token_amount(self, amount: int):
        res = self.__repository.get_by_id(GameStatus.id)
        assert res is not None
        res.total_balance += amount
        self.__repository.update(res)
