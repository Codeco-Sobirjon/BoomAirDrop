from backend.domain.photo.entity import AnalyzisData, PhotoMetadata
from backend.domain.user.entity import User
from backend.infrastructure.photo.model import PhotoMetadataModel
from ..seedwork.mapper import IObjectMapper


class PhotoMetadataModelMapper(IObjectMapper[PhotoMetadata, PhotoMetadataModel]):

    def from_obj(
        self,
        obj: PhotoMetadata,
    ) -> PhotoMetadataModel:

        return PhotoMetadataModel(
            id=obj.id,
            added=obj.added,
            extension=obj.extension,
            user_id=obj.user.id,
            analyzis_data__sad=obj.analyzis_data.sad,
            analyzis_data__angry=obj.analyzis_data.angry,
            analyzis_data__disgust=obj.analyzis_data.disgust,
            analyzis_data__fear=obj.analyzis_data.fear,
            analyzis_data__happy=obj.analyzis_data.happy,
            analyzis_data__neutral=obj.analyzis_data.neutral,
            analyzis_data__surprise=obj.analyzis_data.surprise,
        )

    def to_obj(
        self,
        obj: PhotoMetadataModel,
        user: User | None = None,
    ) -> PhotoMetadata:
        assert user is not None

        mapped_analyzis_data = AnalyzisData(
            sad=obj.analyzis_data__sad,
            angry=obj.analyzis_data__angry,
            disgust=obj.analyzis_data__disgust,
            fear=obj.analyzis_data__fear,
            happy=obj.analyzis_data__happy,
            neutral=obj.analyzis_data__neutral,
            surprise=obj.analyzis_data__surprise,
        )
        return PhotoMetadata(
            id=obj.id,
            added=obj.added,
            extension=obj.extension,
            user=user,
            analyzis_data=mapped_analyzis_data,
        )
