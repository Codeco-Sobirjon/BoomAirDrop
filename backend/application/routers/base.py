from fastapi import APIRouter
from backend.application.routers import game, videos
import backend.application.routers.users as users
import backend.application.routers.photos as photos
from backend.application.routers import referals

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(photos.router, prefix="/photos", tags=["photos"])
router.include_router(game.router, prefix="/game", tags=["game"])
router.include_router(referals.router, prefix="/referals", tags=["referal"])
router.include_router(videos.router, prefix="/videos", tags=["videos"])
