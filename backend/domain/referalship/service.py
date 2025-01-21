from typing import List

from backend import constants as const
from backend.domain.game.service import GameService
from backend.domain.referalship.entity import ReferalCounts, Referalship
from backend.domain.referalship.repository import IReferalshipRepository
from backend.domain.user.entity import User
from backend.domain.user.repository import IUserRepository
from backend import config as conf


class ReferalshipService:
    def __init__(
        self,
        referaship_repository: IReferalshipRepository,
        user_repository: IUserRepository,
        game_service: GameService,
    ):
        self.__repository = referaship_repository
        self.__user_repository = user_repository
        self.__game_service = game_service

    def send_interest_to_invitor(self, referal: User, income: int, iteration: int = 0):
        if iteration >= 2:
            return

        referalship = self.__repository.get_referalship_for_referal(referal)
        if referalship is None:
            return

        percent = (
            const.INVITOR_REWARD_PERCENT
            if iteration == 0
            else const.INVITOR_SECONDARY_REWARD_PERCENT
        )

        reward = round(percent * income / 100)

        referalship.interest_earned += reward
        self.__game_service.increase_token_amount(reward)

        invitor = referalship.invitor
        invitor.balance += reward

        self.__user_repository.update(invitor)
        self.__repository.update(referalship)

        self.send_interest_to_invitor(invitor, income, iteration + 1)

    def assign_referal(self, invitor: User, referal: User):
        referalship = Referalship(
            referal=referal,
            invitor=invitor,
            invitation_reward=const.INVITATION_REWARD,
            interest_earned=0,
        )

        reward = (
            const.INVITATION_PREMIUM_REWARD
            if referal.is_premium
            else const.INVITATION_REWARD
        )
        invitor.balance += reward
        self.send_interest_to_invitor(referal=invitor, income=reward)

        referal.balance += reward
        self.__game_service.increase_token_amount(reward * 2)

        self.__repository.create(referalship)

        self.__user_repository.update(invitor)
        self.__user_repository.update(referal)

    def get_referalships_for_invitor(
        self, invitor: User, limit: int, offset: int
    ) -> List[Referalship]:
        return self.__repository.get_referalships_for_invitor(invitor, limit, offset)

    def get_referal_counts_for_invitor(self, invitor: User) -> ReferalCounts:
        return self.__repository.get_referal_counts_for_invitor(invitor)

    def get_earned_from_referals_for_invitor(self, invitor: User) -> int:
        return self.__repository.get_earned_from_referals_for_invitor(invitor)

    def get_referal_url_for_invitor(self, invitor: User) -> str:
        return "".join([conf.APP_URL, const.REFERAL_PARAM_PREFIX, str(invitor.id)])

    def get_invitor_from_start_param(self, start_param: str) -> User | None:
        invitor_id = start_param[len("friendId") :]
        if not invitor_id.isnumeric():
            return None

        return self.__user_repository.get_by_id(int(invitor_id))
