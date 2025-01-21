from dataclasses import dataclass
from backend.domain.seedwork.entity import Entity


@dataclass()
class GameStatus(Entity[int]):
    id = 1
    total_balance: int
    total_users: int
