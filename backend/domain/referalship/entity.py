from ..user.entity import User
from dataclasses import dataclass


@dataclass()
class Referalship:
    referal: User
    invitor: User
    interest_earned: int
    invitation_reward: int


@dataclass(frozen=True)
class ReferalCounts:
    basic: int
    premium: int
