import unittest
from dataclasses import replace
from datetime import datetime
from typing import Tuple
from unittest.mock import Mock
from uuid import uuid4

import backend.constants as const
from backend.domain.game.service import GameService
from backend.domain.photo.entity import AnalyzisData, Photo, PhotoMetadata
from backend.domain.photo.service import PhotoService
from backend.domain.referalship.service import ReferalshipService
from backend.domain.user.entity import User
from backend.domain.user.port import IProfilePhotoDownloader
from backend.domain.user.repository import IUserRepository
from backend.domain.user.service import UserService


def create_dummies() -> Tuple[User, Photo, PhotoMetadata]:
    user = User(
        id=121,
        name="Dummy",
        profile_photo_path=None,
        verification_photo_metadata=None,
        balance=0,
        language="en",
        is_premium=False,
    )
    photo = bytes([1, 2, 3])
    photo_metadata = PhotoMetadata(
        id=uuid4(),
        user=user,
        added=datetime.now(),
        analyzis_data=AnalyzisData(
            angry=0, disgust=0, fear=0, happy=0, sad=0, surprise=0, neutral=0
        ),
        extension="png",
    )
    user.verification_photo_metadata = photo_metadata
    return user, photo, photo_metadata


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.user_repository = Mock(spec=IUserRepository)
        self.photo_service = Mock(spec=PhotoService)
        self.profile_photo_downloader = Mock(spec=IProfilePhotoDownloader)
        self.game_service = Mock(spec=GameService)
        self.referalship_service = Mock(spec=ReferalshipService)
        self.user_service = UserService(
            self.user_repository,
            self.photo_service,
            self.profile_photo_downloader,
            self.game_service,
            self.referalship_service,
        )

    def test_register_user(self):
        # Given
        (user, photo, photo_metadata) = create_dummies()
        start_param = "friendId212121"
        self.photo_service.save_photo_without_checks.return_value = photo_metadata
        self.profile_photo_downloader.try_download_and_get_path.return_value = None
        self.referalship_service.get_invitor_from_start_param.return_value = user

        # When
        self.user_service.register_user(
            id=user.id,
            name=user.name,
            verification_photo=photo,
            is_premium=user.is_premium,
            language=user.language,
            start_param=start_param,
        )

        # Then
        self.user_repository.create.assert_called_once_with(user)
        self.profile_photo_downloader.try_download_and_get_path.assert_called_once_with(
            user.id
        )
        self.photo_service.save_photo_without_checks.assert_called_once_with(
            user, photo
        )
        self.user_repository.update.assert_called_once_with(user)
        self.referalship_service.get_invitor_from_start_param.assert_called_once_with(
            start_param
        )
        self.referalship_service.assign_referal.assert_called_once()

    def test_get_user_by_id(self):
        # Given
        (user, _, _) = create_dummies()
        self.user_repository.get_by_id.return_value = user

        # When
        result = self.user_service.get_user_by_id(user.id)

        # Then
        self.user_repository.get_by_id.assert_called_once_with(user.id)
        self.assertEqual(user, result)

    def test_get_user_by_not_existing_id(self):
        # Given
        self.user_repository.get_by_id.return_value = None

        # When
        result = self.user_service.get_user_by_id(666)

        # Then
        self.user_repository.get_by_id.assert_called_once_with(666)
        self.assertEqual(result, None)

    def test_try_submit_new_photo(self):
        # Given
        (user, photo, photo_metadata) = create_dummies()
        self.photo_service.try_save_new_photo.return_value = photo_metadata
        user_copy = replace(user)

        # When
        result = self.user_service.try_submit_new_photo(user_copy, photo)

        # Then
        self.assertTrue(result)
        self.photo_service.try_save_new_photo.assert_called_once_with(user_copy, photo)
        self.user_repository.update.assert_called_once_with(user_copy)
        self.referalship_service.send_interest_to_invitor.assert_called_once()
        user_copy = self.user_repository.update.call_args[0][0]
        self.assertEqual(
            user.balance + const.USER_PHOTO_SUBMISSION_REWARD, user_copy.balance
        )


if __name__ == "__main__":
    unittest.main()
