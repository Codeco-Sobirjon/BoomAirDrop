from uuid import UUID
from backend.domain.seedwork.repository import ICrudRepository
from backend.domain.user.entity import User
from backend.domain.video.entitry import VideoMetadata

from abc import ABC, abstractmethod


class IVideoMetadataRepository(ICrudRepository[UUID, VideoMetadata], ABC):

    @abstractmethod
    def get_user_videos(
        self, user: User, limit: int, offset: int
    ) -> list[VideoMetadata]:
        pass

    @abstractmethod
    def get_count_for_user(self, user: User) -> int:
        pass
