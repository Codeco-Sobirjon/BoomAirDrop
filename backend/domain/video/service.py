from datetime import datetime
from uuid import UUID, uuid4
from backend import constants
from backend.domain.photo.service import PhotoService
from backend.domain.user.entity import User
from backend.domain.video.entitry import VideoMetadata
from backend.domain.video.port import (
    IVideoCreator,
    IVideoPublisher,
    IVideoStorage,
)
from backend.domain.video.repository import IVideoMetadataRepository


class VideoService:
    def __init__(
        self,
        video_repository: IVideoMetadataRepository,
        video_creator: IVideoCreator,
        video_storage: IVideoStorage,
        video_publisher: IVideoPublisher,
        photo_service: PhotoService,
    ):
        self.__video_repository = video_repository
        self.__video_storage = video_storage
        self.__photo_service = photo_service
        self.__video_creator = video_creator
        self.__video_publisher = video_publisher

    def create_video_for_user_if_enough_photos(self, user: User, fps: int = 4):
        if (
            self.__photo_service.get_photo_count_for_user(user)
            < constants.VIDEO_MIN_PHOTOS
        ):
            return

        photos = self.__photo_service.get_last_photos_for_user(user)
        video = self.__video_creator.create_video(photos, fps=fps)
        path = self.__video_storage.save_and_get_path(video)
        reward = (
            min(len(photos), constants.VIDEO_MAX_PHOTOS)
            * constants.VIDEO_TOKENS_PER_PHOTO
        )
        metadate = VideoMetadata(
            id=uuid4(),
            user=user,
            path=path,
            created_at=datetime.now(),
            publication_reward=reward,
        )
        self.__video_repository.create(metadate)
        self.__photo_service.delete_last_photos_for_user(user)

    def publish_video_for_user(
        self,
        video_metadata: VideoMetadata,
        comment: str,
        user: User,
    ):
        assert video_metadata.published is False
        video = self.__video_storage.get_by_path(video_metadata.path)
        self.__video_publisher.publish(video, comment, user)
        video_metadata.published = True
        self.__video_repository.update(video_metadata)

    def get_user_videos(self, user: User, limit: int, offset: int):
        return self.__video_repository.get_user_videos(user, limit, offset)

    def get_video_metadata_by_id(self, id: UUID) -> VideoMetadata | None:
        return self.__video_repository.get_by_id(id)

    def get_vieo_count_from_user(self, user: User) -> int:
        return self.__video_repository.get_count_for_user(user)
