from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend.application.mapper.video_schema_mapper import VideoSchemaMapper
import backend.config as cfg
from backend.domain.game.repository import IGameRepository
from backend.domain.referalship.repository import IReferalshipRepository
from backend.domain.referalship.service import ReferalshipService
from backend.domain.video.port import IVideoCreator, IVideoPublisher, IVideoStorage
from backend.domain.video.service import VideoService
from backend.domain.video.repository import IVideoMetadataRepository
from backend.infrastructure.game.mapper import GameStatusModelMapper
from backend.domain.game.service import GameService
from backend.domain.photo.port import (
    IPhotoAnalyzer,
    IPhotoExtensionGuesser,
    IPhotoStorage,
)
from backend.domain.photo.repository import IPhotoMetadataRepository
from backend.domain.photo.service import PhotoService
from backend.domain.user.port import IProfilePhotoDownloader
from backend.domain.user.repository import IUserRepository
from backend.domain.user.service import UserService
from backend.infrastructure.game.repository import GameRepository
from backend.infrastructure.photo.deepface_photo_analyzer import DeepfacePhotoAnalyzer
from backend.infrastructure.photo.filetype_photo_extension_guesser import (
    FiletypePhotoExtensionGuesser,
)
from backend.infrastructure.video.ffmpeg_video_creator import FfmpegVideoCreator
from backend.infrastructure.video.mapper import VideoMetadataModelMapper
from backend.infrastructure.video.fs_video_storage import FSVideoStorage
from backend.infrastructure.video.repository import VideoMetadataRepository
from backend.infrastructure.photo.fs_photo_storage import FSPhototStorage
from backend.infrastructure.photo.mapper import PhotoMetadataModelMapper
from backend.infrastructure.photo.repository import PhotoMetadataRepository
from backend.infrastructure.referalship.mapper import ReferalshipModelMapper
from backend.infrastructure.referalship.repository import ReferalshipRepository
from backend.infrastructure.user.mapper import UserModelMapper
from backend.infrastructure.user.profile_photo_downloader import ProfilePhotoDownloader
from backend.infrastructure.user.repository import UserRepository
from backend.infrastructure.video.video_publisher import TelegramDMVideoPublisher

SessionFactory = sessionmaker(
    bind=create_engine(cfg.DB_DSN, pool_pre_ping=True),
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def create_session() -> Iterator[Session]:
    session = SessionFactory()

    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def photo_analyzer() -> IPhotoAnalyzer:
    return DeepfacePhotoAnalyzer()


def photo_extension_guesser() -> IPhotoExtensionGuesser:
    return FiletypePhotoExtensionGuesser()


def photo_storage() -> IPhotoStorage:
    return FSPhototStorage()


def photo_mapper() -> PhotoMetadataModelMapper:
    return PhotoMetadataModelMapper()


def photo_repository(
    session: Annotated[Session, Depends(create_session)],
    photo_mapper: Annotated[PhotoMetadataModelMapper, Depends(photo_mapper)],
) -> IPhotoMetadataRepository:
    return PhotoMetadataRepository(session, photo_mapper)


def photo_service(
    photo_repository: Annotated[IPhotoMetadataRepository, Depends(photo_repository)],
    photo_storage: Annotated[IPhotoStorage, Depends(photo_storage)],
    photo_extension_guesser: Annotated[
        IPhotoExtensionGuesser, Depends(photo_extension_guesser)
    ],
    photo_analyzer: Annotated[IPhotoAnalyzer, Depends(photo_analyzer)],
) -> PhotoService:
    return PhotoService(
        photo_repository, photo_storage, photo_analyzer, photo_extension_guesser
    )


def user_mapper(
    photo_mapper: Annotated[PhotoMetadataModelMapper, Depends(photo_mapper)]
) -> UserModelMapper:
    return UserModelMapper(photo_mapper)


def user_repository(
    session: Annotated[Session, Depends(create_session)],
    user_mapper: Annotated[UserModelMapper, Depends(user_mapper)],
) -> IUserRepository:
    return UserRepository(session, user_mapper)


def profile_photo_downloader() -> IProfilePhotoDownloader:
    return ProfilePhotoDownloader()


def game_mapper() -> GameStatusModelMapper:
    return GameStatusModelMapper()


def game_repository(
    session: Annotated[Session, Depends(create_session)],
    game_mapper: Annotated[GameStatusModelMapper, Depends(game_mapper)],
) -> IGameRepository:
    return GameRepository(session, game_mapper)


def game_service(
    game_repository: Annotated[IGameRepository, Depends(game_repository)],
) -> GameService:
    return GameService(game_repository)


def referalship_mapper(
    user_mapper: Annotated[UserModelMapper, Depends(user_mapper)]
) -> ReferalshipModelMapper:
    return ReferalshipModelMapper(user_mapper)


def referalship_repository(
    session: Annotated[Session, Depends(create_session)],
    referalship_mapper: Annotated[ReferalshipModelMapper, Depends(referalship_mapper)],
) -> IReferalshipRepository:
    return ReferalshipRepository(session, referalship_mapper)


def referalship_service(
    referalship_repository: Annotated[
        IReferalshipRepository, Depends(referalship_repository)
    ],
    user_repository: Annotated[IUserRepository, Depends(user_repository)],
    game_service: Annotated[GameService, Depends(game_service)],
):
    return ReferalshipService(referalship_repository, user_repository, game_service)


def video_mapper(
    user_mapper: Annotated[UserModelMapper, Depends(user_mapper)]
) -> VideoMetadataModelMapper:
    return VideoMetadataModelMapper(user_mapper)


def video_repository(
    session: Annotated[Session, Depends(create_session)],
    video_mapper: Annotated[VideoMetadataModelMapper, Depends(video_mapper)],
) -> IVideoMetadataRepository:
    return VideoMetadataRepository(session, video_mapper)


def video_creator() -> IVideoCreator:
    return FfmpegVideoCreator()


def video_storage() -> IVideoStorage:
    return FSVideoStorage()


def video_publisher() -> IVideoPublisher:
    return TelegramDMVideoPublisher()


def video_service(
    video_repository: Annotated[IVideoMetadataRepository, Depends(video_repository)],
    video_creator: Annotated[IVideoCreator, Depends(video_creator)],
    video_storage: Annotated[IVideoStorage, Depends(video_storage)],
    video_publisher: Annotated[IVideoPublisher, Depends(video_publisher)],
    photo_service: Annotated[PhotoService, Depends(photo_service)],
) -> VideoService:
    return VideoService(
        video_repository, video_creator, video_storage, video_publisher, photo_service
    )


def user_service(
    user_repository: Annotated[IUserRepository, Depends(user_repository)],
    photo_service: Annotated[PhotoService, Depends(photo_service)],
    profile_photo_downloader: Annotated[
        IProfilePhotoDownloader, Depends(profile_photo_downloader)
    ],
    game_service: Annotated[GameService, Depends(game_service)],
    referalship_service: Annotated[ReferalshipService, Depends(referalship_service)],
    video_service: Annotated[VideoService, Depends(video_service)],
):
    return UserService(
        user_repository,
        photo_service,
        profile_photo_downloader,
        game_service,
        referalship_service,
        video_service,
    )
