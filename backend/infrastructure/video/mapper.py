from backend.domain.video.entitry import VideoMetadata
from backend.infrastructure.seedwork.mapper import IObjectMapper
from backend.infrastructure.video.model import VideoMetadataModel
from backend.infrastructure.user.mapper import UserModelMapper


class VideoMetadataModelMapper(IObjectMapper[VideoMetadata, VideoMetadataModel]):
    def __init__(self, user_mapper: UserModelMapper):
        self.__user_mapper = user_mapper

    def from_obj(self, obj: VideoMetadata) -> VideoMetadataModel:
        return VideoMetadataModel(
            id=obj.id,
            user_id=obj.user.id,
            publication_reward=obj.publication_reward,
            created_at=obj.created_at,
            published=obj.published,
            path=obj.path,
        )

    def to_obj(self, obj: VideoMetadataModel) -> VideoMetadata:
        return VideoMetadata(
            id=obj.id,
            user=self.__user_mapper.to_obj(obj.user),
            path=obj.path,
            publication_reward=obj.publication_reward,
            created_at=obj.created_at,
            published=obj.published,
        )
