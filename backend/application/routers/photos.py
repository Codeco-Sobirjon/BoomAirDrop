from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, HTTPException, status

from backend.application.authorization.tg_miniapp_init_authorization import (
    InitDataUser,
    tg_miniapp_header_init_authorization,
)
from backend.application.deps import user_service
from backend.application.schema.photo import PhotoSubmissionResponse
from backend.domain.user.service import UserService

router = APIRouter()


@router.post("/submit")
def submit(
    auth_user: Annotated[InitDataUser, Depends(tg_miniapp_header_init_authorization)],
    photo: UploadFile,
    user_service: Annotated[UserService, Depends(user_service)],
) -> PhotoSubmissionResponse:

    user = user_service.get_user_by_id(auth_user.id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No user with such id"
        )

    result = user_service.try_submit_new_photo(user, photo.file.read())
    return PhotoSubmissionResponse(success=result)
