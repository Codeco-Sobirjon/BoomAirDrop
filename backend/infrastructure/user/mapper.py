from backend.domain.user import entity
from backend.infrastructure.user.model import UserModel
from ..seedwork.mapper import IObjectMapper
from backend.domain.user.entity import User
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.infrastructure.photo.mapper import PhotoMetadataModelMapper


class UserModelMapper(IObjectMapper[User, UserModel]):
    def __init__(self, photo_mapper: "PhotoMetadataModelMapper"):
        self.__photo_mapper = photo_mapper

    def from_obj(
        self,
        obj: User,
    ) -> UserModel:

        verification_photo_metadata_id = (
            obj.verification_photo_metadata.id
            if obj.verification_photo_metadata
            else None
        )

        model = UserModel(
            id=obj.id,
            name=obj.name,
            profile_photo_path=obj.profile_photo_path,
            balance=obj.balance,
            verification_photo_metadata_id=verification_photo_metadata_id,
            is_premium=obj.is_premium,
            language=obj.language,
        )
        return model

    def to_obj(
        self,
        obj: UserModel,
    ) -> User:
        user = User(
            id=obj.id,
            name=obj.name,
            profile_photo_path=obj.profile_photo_path,
            verification_photo_metadata=None,
            balance=obj.balance,
            is_premium=obj.is_premium,
            language=obj.language,
        )

        metadata = obj.verification_photo_metadata
        assert self.__photo_mapper is not None, "Please provice photo mapper"
        if metadata is not None:
            user.verification_photo_metadata = self.__photo_mapper.to_obj(
                metadata, user=user
            )

        return user
