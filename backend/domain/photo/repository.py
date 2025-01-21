from abc import abstractmethod
from uuid import UUID

from backend.domain.photo.entity import PhotoMetadata
from backend.domain.seedwork.repository import ICrudRepository
from backend.domain.user.entity import User


class IPhotoMetadataRepository(ICrudRepository[UUID, PhotoMetadata]):

    @abstractmethod
    def get_last_n_for_user(self, n: int, user: User) -> list[PhotoMetadata]:
        raise NotImplementedError

    @abstractmethod
    def get_all_for_user_in_creation_order(self, user: User) -> list[PhotoMetadata]:
        raise NotImplementedError

    @abstractmethod
    def count_photos_for_user(self, user: User) -> int:
        raise NotImplementedError

    @abstractmethod
    def delete_list(self, photos: list[PhotoMetadata]):
        raise NotImplementedError
