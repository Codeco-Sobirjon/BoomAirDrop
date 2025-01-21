from backend.domain.photo.port import IPhotoStorage
from backend.domain.photo.entity import Photo, PhotoMetadata

import backend.config as cfg
import os


class FSPhototStorage(IPhotoStorage):
    @staticmethod
    def __get_filename(photo_metadata: PhotoMetadata) -> str:
        return str(photo_metadata.id) + "." + photo_metadata.extension

    @staticmethod
    def __get_path(photo_metadata: PhotoMetadata) -> str:
        filename = FSPhototStorage.__get_filename(photo_metadata)
        path = os.path.join(
            cfg.PHOTO_STORAGE_PATH, str(photo_metadata.user.id), filename
        )
        return path

    def save(self, photo: Photo, photo_metadata: PhotoMetadata):
        path = self.__get_path(photo_metadata)
        dest_dir = os.path.dirname(path)
        os.makedirs(dest_dir, exist_ok=True)
        with open(path, "wb") as f:
            f.write(photo)

    def get(self, photo_metadata: PhotoMetadata) -> Photo:
        path = self.__get_path(photo_metadata)
        with open(path, "rb") as f:
            return f.read()

    def delete(self, photo_metadata: PhotoMetadata):
        path = self.__get_path(photo_metadata)
        os.remove(path)
