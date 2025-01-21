from uuid import UUID

from sqlalchemy.orm import Session
from backend.domain.photo.entity import PhotoMetadata
from backend.domain.photo.repository import IPhotoMetadataRepository
from backend.infrastructure.photo.mapper import PhotoMetadataModelMapper
from backend.infrastructure.photo.model import PhotoMetadataModel
from backend.infrastructure.seedwork.repository import SqlAlchemyCrudRepository
from backend.domain.user.entity import User


class PhotoMetadataRepository(
    IPhotoMetadataRepository,
    SqlAlchemyCrudRepository[UUID, PhotoMetadataModel, PhotoMetadata],
):
    model_class = PhotoMetadataModel

    def __init__(self, session: Session, object_mapper: PhotoMetadataModelMapper):
        self._session = session
        self._object_mapper: PhotoMetadataModelMapper = object_mapper

    def get_last_n_for_user(self, n: int, user: User) -> list[PhotoMetadata]:
        res = (
            self._session.query(self.model_class)
            .order_by(PhotoMetadataModel.added.desc())
            .filter_by(user_id=user.id)
            .limit(n)
        )

        return [self._object_mapper.to_obj(m, user=user) for m in res.all()]

    def delete(self, entity: PhotoMetadata):
        raise NotImplementedError

    def delete_list(self, photos: list[PhotoMetadata]):
        ids = list(map(lambda p: p.id, photos))
        self._session.query(PhotoMetadataModel).filter(
            PhotoMetadataModel.id.in_(ids)
        ).delete()

    def get_all_for_user_in_creation_order(self, user: User) -> list[PhotoMetadata]:
        assert user.verification_photo_metadata is not None
        models = (
            self._session.query(PhotoMetadataModel)
            .filter(
                PhotoMetadataModel.id != user.verification_photo_metadata.id,
                PhotoMetadataModel.user_id == user.id,
            )
            .order_by(PhotoMetadataModel.added)
            .all()
        )
        return [self._object_mapper.to_obj(m, user=user) for m in models]

    def count_photos_for_user(self, user: User) -> int:
        assert user.verification_photo_metadata is not None
        return (
            self._session.query(PhotoMetadataModel)
            .filter(
                PhotoMetadataModel.user_id == user.id,
                PhotoMetadataModel.id != user.verification_photo_metadata.id,
            )
            .count()
        )
