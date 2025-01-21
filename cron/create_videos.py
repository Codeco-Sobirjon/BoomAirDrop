from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from backend import config
from backend.application.deps import video_creator
from backend.domain.game.service import GameService
from backend.domain.referalship.service import ReferalshipService
from backend.domain.video.service import VideoService
from backend.infrastructure.photo.repository import PhotoMetadataRepository
from backend.domain.photo.service import PhotoService
from backend.domain.user.service import UserService
from backend.infrastructure.referalship.mapper import ReferalshipModelMapper
from backend.infrastructure.user.repository import UserRepository
from backend.infrastructure.photo.mapper import PhotoMetadataModelMapper
from backend.infrastructure.user.mapper import UserModelMapper
from backend.infrastructure.user.profile_photo_downloader import ProfilePhotoDownloader
from backend.infrastructure.photo.fs_photo_storage import FSPhototStorage
from backend.infrastructure.photo.deepface_photo_analyzer import DeepfacePhotoAnalyzer
from backend.infrastructure.photo.filetype_photo_extension_guesser import (
    FiletypePhotoExtensionGuesser,
)
from backend.infrastructure.game.repository import GameRepository
from backend.infrastructure.game.mapper import GameStatusModelMapper
from backend.infrastructure.referalship.repository import ReferalshipRepository
from backend.infrastructure.video.fs_video_storage import FSVideoStorage
from backend.infrastructure.video.mapper import VideoMetadataModelMapper
from backend.infrastructure.video.repository import VideoMetadataRepository
from backend.infrastructure.video.ffmpeg_video_creator import FfmpegVideoCreator
from backend.infrastructure.video.video_publisher import TelegramDMVideoPublisher

engine = create_engine(config.DB_DSN)

with Session(engine) as session:
    photo_mapper = PhotoMetadataModelMapper()

    user_mapper = UserModelMapper(photo_mapper)
    user_repository = UserRepository(session, user_mapper)

    photo_repository = PhotoMetadataRepository(session, photo_mapper)
    photo_storage = FSPhototStorage()
    photo_analyzer = DeepfacePhotoAnalyzer()
    photo_ext_guesser = FiletypePhotoExtensionGuesser()

    photo_service = PhotoService(
        photo_repository, photo_storage, photo_analyzer, photo_ext_guesser
    )

    game_mapper = GameStatusModelMapper()
    game_repository = GameRepository(session, game_mapper)
    game_service = GameService(game_repository)

    referalship_mapper = ReferalshipModelMapper(user_mapper)
    referalship_repository = ReferalshipRepository(session, referalship_mapper)
    refe = referalship_repository

    referalship_service = ReferalshipService(
        referalship_repository, user_repository, game_service
    )

    video_mapper = VideoMetadataModelMapper(user_mapper)
    video_repository = VideoMetadataRepository(session, video_mapper)
    video_creator = FfmpegVideoCreator()
    video_storaga = FSVideoStorage()
    video_publisher = TelegramDMVideoPublisher()

    video_service = VideoService(
        video_repository, video_creator, video_storaga, video_publisher, photo_service
    )

    profile_photo_downloader = ProfilePhotoDownloader()
    user_service = UserService(
        user_repository,
        photo_service,
        profile_photo_downloader,
        game_service,
        referalship_service,
        video_service,
    )

    user_service.create_videos_for_all_users()
