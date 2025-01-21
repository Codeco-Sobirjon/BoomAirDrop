import unittest
from backend.domain.photo.entity import AnalyzisData
from backend.domain.photo.service import PhotoService
from backend.domain.photo.repository import IPhotoMetadataRepository
from backend.domain.photo.port import (
    IPhotoExtensionGuesser,
    IPhotoStorage,
    IPhotoAnalyzer,
)
from unittest.mock import Mock

import backend.constants as const

from .test_user_service import create_dummies


def create_different_photo():
    photo = bytes([3, 4, 5])
    parameter_value = const.PHOTO_UNIQUINESS_DIFFERENCE_THRESHOLD // 7 + 2
    analyzis_data = AnalyzisData(
        angry=parameter_value,
        disgust=parameter_value,
        fear=parameter_value,
        happy=parameter_value,
        sad=parameter_value,
        surprise=parameter_value,
        neutral=parameter_value,
    )

    return photo, analyzis_data


def create_same_photo():
    photo = bytes([1, 2, 3])
    parameter_value = 0
    analyzis_data = AnalyzisData(
        angry=parameter_value,
        disgust=parameter_value,
        fear=parameter_value,
        happy=parameter_value,
        sad=parameter_value,
        surprise=parameter_value,
        neutral=parameter_value,
    )

    return photo, analyzis_data


class TestPhotoService:
    def setUp(self):
        self.metadata_repository = Mock(spec=IPhotoMetadataRepository)
        self.photo_storage = Mock(spec=IPhotoStorage)
        self.photo_analyzer = Mock(spec=IPhotoAnalyzer)
        self.extension_guesser = Mock(spec=IPhotoExtensionGuesser)
        self.photo_service = PhotoService(
            self.metadata_repository,
            self.photo_storage,
            self.photo_analyzer,
            self.extension_guesser,
        )

    def test_save_photo_without_checks(self):
        # Given
        (user, photo, photo_metadata) = create_dummies()
        self.photo_analyzer.analyze.return_value = photo_metadata.analyzis_data
        self.extension_guesser.guess.return_value = photo_metadata.extension

        # When
        result = self.photo_service.save_photo_without_checks(user, photo)

        # Then
        self.metadata_repository.create.assert_called_once()
        saved_metadata = self.metadata_repository.create.call_args[0][0]
        self.photo_storage.save.assert_called_once_with(photo, saved_metadata)
        self.extension_guesser.guess.assert_called_once_with(photo)

        self.assertEqual(result, saved_metadata)
        self.assertEqual(result.user, user)
        self.assertEqual(result.analyzis_data, photo_metadata.analyzis_data)

    def base_try_save_new_photo(
        self, same_person: bool, different_expression: bool, asserts
    ):
        (user, photo, photo_metadata) = create_dummies()
        new_photo, new_analyzis_data = (
            create_different_photo() if different_expression else create_same_photo()
        )

        self.photo_storage.get.return_value = photo
        self.photo_analyzer.verify_same_person.return_value = same_person
        self.extension_guesser.guess.return_value = photo_metadata.extension

        self.photo_analyzer.analyze.return_value = new_analyzis_data
        self.metadata_repository.get_last_n_for_user.return_value = [photo_metadata]

        # When
        result = self.photo_service.try_save_new_photo(user, new_photo)

        # Then
        asserts(user, photo, new_photo, new_analyzis_data, result)

    def test_try_save_new_photo(self):
        def asserts(user, photo, new_photo, new_analyzis_data, result):
            self.assertNotEqual(result, None)
            self.photo_analyzer.verify_same_person.assert_called_once_with(
                photo, new_photo
            )
            self.photo_analyzer.analyze.assert_called_once_with(new_photo)
            self.extension_guesser.guess.assert_called_once_with(new_photo)
            self.metadata_repository.create.assert_called_once()
            saved_metadata = self.metadata_repository.create.call_args[0][0]
            self.assertEqual(saved_metadata, result)
            self.assertEqual(saved_metadata.analyzis_data, new_analyzis_data)
            self.assertEqual(saved_metadata.user, user)

        self.base_try_save_new_photo(
            same_person=True, different_expression=True, asserts=asserts
        )

    def test_try_save_new_photo_different_person(self):
        def asserts(_, photo, new_photo, _2, result):
            self.assertEqual(result, None)
            self.photo_analyzer.verify_same_person.assert_called_once_with(
                photo, new_photo
            )
            self.metadata_repository.create.assert_not_called()
            self.photo_storage.assert_not_called()

        self.base_try_save_new_photo(
            same_person=False, different_expression=True, asserts=asserts
        )

    def test_try_save_new_photo_same_expression(self):
        def asserts(_1, _2, new_photo, _3, result):
            self.assertEqual(result, None)
            self.photo_analyzer.analyze.assert_called_once_with(new_photo)
            self.metadata_repository.create.assert_not_called()
            self.photo_storage.assert_not_called()

        self.base_try_save_new_photo(
            same_person=True, different_expression=False, asserts=asserts
        )


if __name__ == "__main__":
    unittest.main()
