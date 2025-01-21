from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from backend import config
from backend.application.authorization.tg_miniapp_init_authorization import (
    InitDataUser,
    tg_miniapp_header_init_authorization,
)
from backend.application.deps import user_service
from backend.application.mapper.user_schema_mapper import UserSchemaMapper
from backend.application.schema import photo
from backend.application.schema.user import UserResponceSchema
from backend.domain.user.service import UserService
import os

router = APIRouter()


@router.post("/register")
def register(
    auth_user: Annotated[InitDataUser, Depends(tg_miniapp_header_init_authorization)],
    verification_photo: UploadFile,
    user_service: Annotated[UserService, Depends(user_service)],
    schema_mapper: Annotated[UserSchemaMapper, Depends()],
) -> UserResponceSchema:

    user = user_service.register_user(
        id=auth_user.id,
        name=auth_user.get_full_name(),
        verification_photo=verification_photo.file.read(),
        is_premium=auth_user.is_premium,
        language=auth_user.language_code,
        start_param=auth_user.start_param,
    )

    return schema_mapper.from_obj(user)


@router.get("/profile")
def get_user(
    user_service: Annotated[UserService, Depends(user_service)],
    auth_user: Annotated[InitDataUser, Depends(tg_miniapp_header_init_authorization)],
    schema_mapper: Annotated[UserSchemaMapper, Depends()],
) -> UserResponceSchema:

    user = user_service.get_user_by_id(auth_user.id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No registerd user with this id",
        )

    return schema_mapper.from_obj(user)


@router.post("/profile")
def update_user(
    user_service: Annotated[UserService, Depends(user_service)],
    auth_user: Annotated[InitDataUser, Depends(tg_miniapp_header_init_authorization)],
):
    user = user_service.get_user_by_id(auth_user.id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No registerd user with this id",
        )

    user_service.update_user_info(
        user,
        name=auth_user.get_full_name(),
        is_premium=auth_user.is_premium,
        language=auth_user.language_code,
    )


@router.get("/profile/photo")
def get_profile_photo(
    user_service: Annotated[UserService, Depends(user_service)],
    auth_user: Annotated[InitDataUser, Depends(tg_miniapp_header_init_authorization)],
):
    user = user_service.get_user_by_id(auth_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.profile_photo_path:
        raise HTTPException(status_code=404, detail="Photo not found")

    photo_path = os.path.join(
        config.PHOTO_PROFILE_STORAGE_PATH, user.profile_photo_path
    )
    if not os.path.exists(photo_path):
        return HTTPException(status_code=404, detail="Photo not found")
    return FileResponse(photo_path)


@router.get("/profile/photo/{id}")
def get_profile_photo_by_id(
    auth_user: Annotated[InitDataUser, Depends(tg_miniapp_header_init_authorization)],
    user_service: Annotated[UserService, Depends(user_service)],
    id: int,
):
    user = user_service.get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.profile_photo_path:
        raise HTTPException(status_code=404, detail="Photo not found")

    photo_path = os.path.join(
        config.PHOTO_PROFILE_STORAGE_PATH, user.profile_photo_path
    )
    if not os.path.exists(photo_path):
        return HTTPException(status_code=404, detail="Photo not found")
    return FileResponse(photo_path)
