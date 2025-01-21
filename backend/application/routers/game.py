from typing import Annotated
from fastapi import APIRouter, Depends
from dataclasses import replace

from backend import constants
from backend.application.authorization.tg_miniapp_init_authorization import (
    InitDataUser,
    tg_miniapp_header_init_authorization,
)
from backend.application.deps import game_service
from backend.domain.game.service import GameService


router = APIRouter()


@router.get("/status")
def get_game_status(
    game_service: Annotated[GameService, Depends(game_service)],
):
    status = game_service.get_game_status()
    status = replace(
        status, total_balance=status.total_balance / constants.USER_BALANCE_PRECISION, id=None
    )
    return status
