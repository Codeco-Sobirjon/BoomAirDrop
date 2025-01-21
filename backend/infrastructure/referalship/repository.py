from sqlalchemy import func
from sqlalchemy.orm import Session
from backend.domain.referalship.entity import ReferalCounts, Referalship
from backend.domain.referalship.repository import IReferalshipRepository
from backend.domain.user.entity import User
from backend.infrastructure.seedwork.mapper import IObjectMapper
from backend.infrastructure.referalship.model import ReferalshipModel
from typing import List

from backend.infrastructure.user.model import UserModel


class ReferalshipRepository(IReferalshipRepository):
    def __init__(
        self, session: Session, mapper: IObjectMapper[Referalship, ReferalshipModel]
    ):
        self.__session = session
        self.__mapper = mapper

    def create(self, referalship: Referalship):
        model = self.__mapper.from_obj(referalship)
        self.__session.add(model)

    def update(self, referalship: Referalship):
        model = self.__mapper.from_obj(referalship)
        self.__session.merge(model)

    def get_referalship_for_referal(self, referal: User) -> Referalship | None:
        model = (
            self.__session.query(ReferalshipModel)
            .where(ReferalshipModel.referal_id == referal.id)
            .first()
        )
        if model is None:
            return None
        return self.__mapper.to_obj(model)

    def get_referalships_for_invitor(
        self, user: User, limit: int, offset: int
    ) -> List[Referalship]:
        models = (
            self.__session.query(ReferalshipModel)
            .where(ReferalshipModel.invitor_id == user.id)
            .order_by(ReferalshipModel.interest_earned.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return list(map(self.__mapper.to_obj, models))

    def get_referal_counts_for_invitor(self, invitor: User) -> ReferalCounts:
        result = (
            self.__session.query(
                UserModel.is_premium,
                func.count(UserModel.is_premium),
            )
            .join(ReferalshipModel.referal)
            .where(ReferalshipModel.invitor_id == invitor.id)
            .group_by(UserModel.is_premium)
        ).all()

        if len(result) == 0:
            return ReferalCounts(basic=0, premium=0)

        basic, premium = 0, 0

        for is_premium, count in result:
            if is_premium:
                premium = count
            else:
                basic = count

        return ReferalCounts(basic=basic, premium=premium)

    def get_earned_from_referals_for_invitor(self, invitor: User) -> int:
        result = (
            self.__session.query(
                func.sum(ReferalshipModel.interest_earned),
                func.sum(ReferalshipModel.invitation_reward),
            )
            .where(ReferalshipModel.invitor_id == invitor.id)
            .one()
        )
        if result[0] is None:
            return 0
        return sum(result)
