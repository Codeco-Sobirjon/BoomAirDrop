from typing import Any

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger

from backend.infrastructure.seedwork.model import Base


class GameStatusModel(Base):
    __tablename__ = "game_status"
    id: Mapped[int] = mapped_column(primary_key=True)
    total_users: Mapped[int] = mapped_column(BigInteger)
    total_balance: Mapped[int] = mapped_column(BigInteger)

    def __init__(self, id: int, total_users: int, total_balance: int, **kw: Any):
        super().__init__(**kw)
        self.id = 1
        self.total_users = total_users
        self.total_balance = total_balance
