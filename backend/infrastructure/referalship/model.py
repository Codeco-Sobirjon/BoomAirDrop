from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.infrastructure.seedwork.model import Base
from backend.infrastructure.user.model import UserModel


class ReferalshipModel(Base):
    __tablename__ = "referal"
    invitor_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), index=True, primary_key=True
    )
    referal_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), index=True, primary_key=True
    )
    invitor: Mapped[UserModel] = relationship(
        UserModel, foreign_keys=[invitor_id], cascade="", viewonly=True
    )
    referal: Mapped[UserModel] = relationship(
        UserModel, foreign_keys=[referal_id], cascade="", viewonly=True
    )
    interest_earned: Mapped[int] = mapped_column(BigInteger)
    invitation_reward: Mapped[int]

    def __init__(
        self,
        invitor_id: int,
        referal_id: int,
        interest_earned: int,
        invitation_reward: int,
    ):
        self.invitor_id = invitor_id
        self.referal_id = referal_id
        self.interest_earned = interest_earned
        self.invitation_reward = invitation_reward
