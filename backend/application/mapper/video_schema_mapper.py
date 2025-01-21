from backend import constants
from backend.application.schema.video import VideoSchema
from backend.domain.video.entitry import VideoMetadata
from backend.infrastructure.seedwork.mapper import IObjectMapper


class VideoSchemaMapper(IObjectMapper[VideoMetadata, VideoSchema]):
    def to_obj(self, obj: VideoSchema) -> VideoMetadata:
        raise NotImplementedError

    def from_obj(self, obj: VideoMetadata) -> VideoSchema:
        return VideoSchema(
            id=obj.id,
            playback_url="/api/videos/get/" + str(obj.id),
            reward=obj.publication_reward / constants.USER_BALANCE_PRECISION,
            created_at=obj.created_at,
            published=obj.published,
        )
