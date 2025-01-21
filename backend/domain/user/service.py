from uuid import UUID
from backend.domain.photo.entity import Photo
from backend.domain.photo.service import PhotoService
from backend.domain.referalship.service import ReferalshipService
from backend.domain.user.port import IProfilePhotoDownloader
from backend.domain.user.repository import IUserRepository
from backend.domain.video.entitry import VideoMetadata
from backend.domain.video.service import VideoService
from .entity import User
import backend.constants as const
from ..game.service import GameService


class UserService:
    def __init__(
        self,
        user_repository: IUserRepository,
        photo_service: PhotoService,
        profile_photo_downloader: IProfilePhotoDownloader,
        game_service: GameService,
        referalship_service: ReferalshipService,
        video_service: VideoService,
    ):
        self.__repository = user_repository
        self.__photo_service = photo_service
        self.__profile_photo_downloader = profile_photo_downloader
        self.__game_service = game_service
        self.__referalship_service = referalship_service
        self.__video_service = video_service

    def get_user_by_id(self, id: int) -> User | None:
        return self.__repository.get_by_id(id)

    def update_user_info(
        self, user: User, name: str, is_premium: bool | None, language: str | None
    ) -> User:
        user.name = name
        user.is_premium = is_premium if is_premium is not None else False
        user.language = language if language is not None else user.language

        profile_photo_path = self.__profile_photo_downloader.try_download_and_get_path(
            user_id=user.id
        )
        user.profile_photo_path = profile_photo_path

        self.__repository.update(user)
        return user

    def register_user(
        self,
        id: int,
        name: str,
        verification_photo: Photo,
        is_premium: bool | None,
        language: str | None,
        start_param: str | None,
    ) -> User:
        profile_photo_path = self.__profile_photo_downloader.try_download_and_get_path(
            id
        )

        is_premium = is_premium if is_premium is not None else False
        language = language if language is not None else "en"

        user = User(
            id,
            name,
            profile_photo_path=profile_photo_path,
            verification_photo_metadata=None,
            balance=0,
            is_premium=is_premium,
            language=language,
        )
        self.__repository.create(user)

        verification_photo_metadata = self.__photo_service.save_photo_without_checks(
            user, verification_photo
        )

        user.verification_photo_metadata = verification_photo_metadata

        if start_param is not None:
            invitor = self.__referalship_service.get_invitor_from_start_param(
                start_param
            )
            if invitor is not None and invitor.id != user.id:
                self.__referalship_service.assign_referal(invitor=invitor, referal=user)

        self.__repository.update(user)
        self.__game_service.increase_user_count()
        return user

    def try_submit_new_photo(self, user: User, photo: Photo) -> bool:
        if self.__photo_service.try_save_new_photo(user, photo):
            user.balance += const.USER_PHOTO_SUBMISSION_REWARD
            self.__game_service.increase_token_amount(
                const.USER_PHOTO_SUBMISSION_REWARD
            )
            self.__referalship_service.send_interest_to_invitor(
                referal=user, income=const.USER_PHOTO_SUBMISSION_REWARD
            )
            self.__repository.update(user)
            return True

        return False

    def try_publish_new_video(
        self, user: User, comment: str, video_metadata: VideoMetadata
    ):
        assert video_metadata.user.id == user.id
        self.__video_service.publish_video_for_user(video_metadata, comment, user)
        user.balance += video_metadata.publication_reward
        self.__game_service.increase_token_amount(video_metadata.publication_reward)
        self.__referalship_service.send_interest_to_invitor(
            user, video_metadata.publication_reward
        )

    def create_videos_for_all_users(self):
        users = self.__repository.get_all()
        for u in users:
            self.__video_service.create_video_for_user_if_enough_photos(u)
