from uuid import UUID

from backend.domain.user.entity import User
from backend.domain.video.entitry import VideoMetadata
from backend.domain.video.repository import IVideoMetadataRepository
from backend.infrastructure.seedwork.repository import SqlAlchemyCrudRepository
from backend.infrastructure.video.model import VideoMetadataModel


class VideoMetadataRepository(
    IVideoMetadataRepository,
    SqlAlchemyCrudRepository[UUID, VideoMetadataModel, VideoMetadata],
):
    model_class = VideoMetadataModel

    def get_user_videos(
        self, user: User, limit: int, offset: int
    ) -> list[VideoMetadata]:
        models = (
            self._session.query(VideoMetadataModel)
            .filter(VideoMetadataModel.user_id == user.id)
            .order_by(VideoMetadataModel.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        return [self._object_mapper.to_obj(m) for m in models]

    def get_count_for_user(self, user: User) -> int:
        return (
            self._session.query(VideoMetadataModel)
            .filter(VideoMetadataModel.user_id == user.id)
            .count()
        )

    def delete(self, entity: VideoMetadata):
        raise NotImplementedError
