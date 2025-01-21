from os import name
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from backend.application.schema.referal import ReferalSchema, ReferalStats
from backend.domain.referalship.service import ReferalshipService
from backend.domain.user.service import UserService
from ..deps import referalship_service, user_service
from backend import constants as const

from backend.application.authorization.tg_miniapp_init_authorization import (
    InitDataUser,
    tg_miniapp_header_init_authorization,
)

router = APIRouter()


@router.get("/link")
def get_referal_link(
    auth_user: Annotated[InitDataUser, Depends(tg_miniapp_header_init_authorization)],
    user_service: Annotated[UserService, Depends(user_service)],
    referal_service: Annotated[ReferalshipService, Depends(referalship_service)],
) -> str:

    user = user_service.get_user_by_id(auth_user.id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return referal_service.get_referal_url_for_invitor(user)


@router.get("/stats")
def get_referal_stats(
    auth_user: Annotated[InitDataUser, Depends(tg_miniapp_header_init_authorization)],
    user_service: Annotated[UserService, Depends(user_service)],
    referal_service: Annotated[ReferalshipService, Depends(referalship_service)],
) -> ReferalStats:
    user = user_service.get_user_by_id(auth_user.id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    referal_counts = referal_service.get_referal_counts_for_invitor(user)
    earned = referal_service.get_earned_from_referals_for_invitor(user)
    return ReferalStats(
        basic_count=referal_counts.basic,
        premium_count=referal_counts.premium,
        earned_tokens=earned / const.USER_BALANCE_PRECISION,
    )


@router.get("/all")
def get_all(
    auth_user: Annotated[InitDataUser, Depends(tg_miniapp_header_init_authorization)],
    user_service: Annotated[UserService, Depends(user_service)],
    referal_service: Annotated[ReferalshipService, Depends(referalship_service)],
    limit: int = 10,
    offset: int = 0,
) -> List[ReferalSchema]:

    user = user_service.get_user_by_id(auth_user.id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    refs = referal_service.get_referalships_for_invitor(user, limit, offset)
    ret = []

    for r in refs:
        ret.append(
            ReferalSchema(
                id=r.referal.id,
                name=r.referal.name,
                earned=r.interest_earned / const.USER_BALANCE_PRECISION,
            )
        )

    return ret
