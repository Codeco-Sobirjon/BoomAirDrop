from backend.domain.referalship.entity import Referalship
from backend.infrastructure.referalship.model import ReferalshipModel
from backend.infrastructure.seedwork.mapper import IObjectMapper
from backend.infrastructure.user.mapper import UserModelMapper


class ReferalshipModelMapper(IObjectMapper[Referalship, ReferalshipModel]):
    def __init__(self, user_mapper: UserModelMapper):
        self.__user_mapper = user_mapper

    def from_obj(self, obj: Referalship) -> ReferalshipModel:
        return ReferalshipModel(
            invitor_id=obj.invitor.id,
            referal_id=obj.referal.id,
            interest_earned=obj.interest_earned,
            invitation_reward=obj.invitation_reward,
        )

    def to_obj(self, obj: ReferalshipModel) -> Referalship:
        return Referalship(
            invitor=self.__user_mapper.to_obj(obj.invitor),
            referal=self.__user_mapper.to_obj(obj.referal),
            interest_earned=obj.interest_earned,
            invitation_reward=obj.invitation_reward,
        )
