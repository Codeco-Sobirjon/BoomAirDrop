from abc import ABC, abstractmethod
from .entity import Referalship, ReferalCounts
from ..user.entity import User
from typing import List


class IReferalshipRepository(ABC):

    @abstractmethod
    def create(self, referalship: Referalship):
        raise NotImplementedError

    @abstractmethod
    def update(self, referalship: Referalship):
        raise NotImplementedError

    @abstractmethod
    def get_referalship_for_referal(self, referal: User) -> Referalship | None:
        raise NotImplementedError

    @abstractmethod
    def get_referalships_for_invitor(
        self, user: User, limit: int, offset: int
    ) -> List[Referalship]:
        raise NotImplementedError

    @abstractmethod
    def get_referal_counts_for_invitor(self, invitor: User) -> ReferalCounts:
        raise NotImplementedError

    @abstractmethod
    def get_earned_from_referals_for_invitor(self, invitor: User) -> int:
        raise NotImplementedError
