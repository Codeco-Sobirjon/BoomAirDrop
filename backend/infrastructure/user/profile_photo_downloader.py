from pydantic import BaseModel
from backend.domain.user.port import IProfilePhotoDownloader
import backend.config as cfg
import httpx
from typing import Optional
import os


class PhotoSize(BaseModel):
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: Optional[int] = None


class UserProfilePhotos(BaseModel):
    total_count: int
    photos: list[list[PhotoSize]]


class File(BaseModel):
    file_id: str
    file_unique_id: str
    file_size: Optional[int] = None
    file_path: Optional[str] = None


class ProfilePhotoDownloader(IProfilePhotoDownloader):
    def __init__(self):
        os.makedirs(cfg.PHOTO_PROFILE_STORAGE_PATH, exist_ok=True)

    @staticmethod
    def __get_photo_file_id(user_id: int) -> str | None:
        r = httpx.get(
            f"https://api.telegram.org/bot{cfg.BOT_TOKEN}/getUserProfilePhotos?user_id={user_id}"
        )

        json = r.json()
        if not json["ok"]:
            return None

        result = UserProfilePhotos.model_validate(json["result"])
        if len(result.photos) == 0:
            return None

        return result.photos[0][0].file_id

    @staticmethod
    def __get_tg_file_path(file_id: str) -> str | None:
        r = httpx.get(
            f"https://api.telegram.org/bot{cfg.BOT_TOKEN}/getFile?file_id={file_id}"
        )

        json = r.json()
        if not json["ok"]:
            return None

        file = File.model_validate(json["result"])
        return file.file_path

    def try_download_and_get_path(self, user_id: int) -> str | None:
        file_id = self.__get_photo_file_id(user_id)

        if not file_id:
            return None

        tg_file_path = self.__get_tg_file_path(file_id)
        if tg_file_path is None:
            return None

        r = httpx.get(
            "https://api.telegram.org/file/bot" + cfg.BOT_TOKEN + "/" + tg_file_path
        )
        if r.status_code != 200:
            return None

        file_ext = os.path.splitext(tg_file_path)[1]
        file_name = f"{user_id}{file_ext}"

        with open(os.path.join(cfg.PHOTO_PROFILE_STORAGE_PATH, file_name), "wb") as f:
            f.write(r.content)

        return file_name
