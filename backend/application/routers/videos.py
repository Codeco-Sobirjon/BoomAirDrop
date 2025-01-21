from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from backend import config
from backend.application.authorization.tg_miniapp_init_authorization import (
    InitDataUser,
    tg_miniapp_header_init_authorization,
)
from backend.application.deps import user_service, video_service
from backend.application.mapper.video_schema_mapper import VideoSchemaMapper
from backend.application.schema.video import VideoPublisRequest, VideoResponseSchema
from backend.domain.user.service import UserService
from backend.domain.video.service import VideoService

router = APIRouter()


@router.get("/create")
def create_video(
    auth_user: Annotated[InitDataUser, Depends(tg_miniapp_header_init_authorization)],
    user_service: Annotated[UserService, Depends(user_service)],
    video_service: Annotated[VideoService, Depends(video_service)],
):
    user = user_service.get_user_by_id(auth_user.id)
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    video_service.create_video_for_user_if_enough_photos(user)


@router.get("/all")
def get_videos(
    auth_user: Annotated[InitDataUser, Depends(tg_miniapp_header_init_authorization)],
    user_service: Annotated[UserService, Depends(user_service)],
    video_service: Annotated[VideoService, Depends(video_service)],
    mapper: Annotated[VideoSchemaMapper, Depends()],
    limit: int,
    offset: int,
) -> VideoResponseSchema:
    user = user_service.get_user_by_id(auth_user.id)
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    vids = video_service.get_user_videos(user, limit, offset)
    video_schemas = [mapper.from_obj(v) for v in vids]
    count = video_service.get_vieo_count_from_user(user)
    return VideoResponseSchema(total=count, videos=video_schemas)


@router.get("/get/{id}")
def get_video(
    id: UUID,
    video_service: Annotated[VideoService, Depends(video_service)],
):
    video = video_service.get_video_metadata_by_id(id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(config.VIDEOS_STORAGE_PATH + "/" + video.path)


@router.post("/publish")
def publish_video(
    req: VideoPublisRequest,
    auth_user: Annotated[InitDataUser, Depends(tg_miniapp_header_init_authorization)],
    user_service: Annotated[UserService, Depends(user_service)],
    video_service: Annotated[VideoService, Depends(video_service)],
):
    user = user_service.get_user_by_id(auth_user.id)
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    video = video_service.get_video_metadata_by_id(req.id)
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    user_service.try_publish_new_video(user, req.comment, video)
