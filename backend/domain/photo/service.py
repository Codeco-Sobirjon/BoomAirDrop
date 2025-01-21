from datetime import datetime
from uuid import uuid4
from backend.domain.photo.entity import AnalyzisData, Photo, PhotoMetadata
from backend.domain.user.entity import User
from .repository import IPhotoMetadataRepository
from .port import (
    IPhotoExtensionGuesser,
    IPhotoStorage,
    IPhotoAnalyzer,
)
import backend.constants as const


class PhotoService:
    def __init__(
        self,
        metadata_repository: IPhotoMetadataRepository,
        photo_storage: IPhotoStorage,
        photo_analyzer: IPhotoAnalyzer,
        photo_extension_guesser: IPhotoExtensionGuesser,
    ):
        self.__metadata_repository = metadata_repository
        self.__storage = photo_storage
        self.__analyzer = photo_analyzer
        self.__extension_guesser = photo_extension_guesser

    def __save_photo(
        self, user: User, photo: Photo, analyzis_data: AnalyzisData
    ) -> PhotoMetadata:
        extension = self.__extension_guesser.guess(photo)
        metadata = PhotoMetadata(
            id=uuid4(),
            user=user,
            added=datetime.now(),
            analyzis_data=analyzis_data,
            extension=extension,
        )
        self.__metadata_repository.create(metadata)
        self.__storage.save(photo, metadata)
        return metadata

    def save_photo_without_checks(self, user: User, photo: Photo) -> PhotoMetadata:
        analyzis_data = self.__analyzer.analyze(photo)
        return self.__save_photo(user, photo, analyzis_data)

    @staticmethod
    def __compute_difference(
        analzyis_data1: AnalyzisData, analyzis_data2: AnalyzisData
    ) -> int:
        total_diff = 0
        vars1 = vars(analzyis_data1)
        vars2 = vars(analyzis_data2)
        for k in vars1.keys():
            total_diff += abs(vars1[k] - vars2[k])

        return total_diff

    def __is_expression_unique_for_user(
        self, user: User, analyzis_data: AnalyzisData
    ) -> bool:
        photo_metadatas = self.__metadata_repository.get_last_n_for_user(
            const.PHOTO_AMOUNT_FOR_UNIQUINESS_CHECK, user
        )

        for m in photo_metadatas:
            diff = self.__compute_difference(m.analyzis_data, analyzis_data)
            if diff < const.PHOTO_UNIQUINESS_DIFFERENCE_THRESHOLD:
                return False

        return True

    def __is_user_present_on_photo(self, user: User, photo: Photo) -> bool:
        # Should be true for registered users
        assert user.verification_photo_metadata is not None

        verification_photo = self.__storage.get(user.verification_photo_metadata)
        result = self.__analyzer.verify_same_person(verification_photo, photo)

        if result:
            return True

        last_metas = self.__metadata_repository.get_last_n_for_user(
            const.PHOTO_VERIFICATION_MAX_RETRIES, user
        )
        for m in last_metas:
            p = self.__storage.get(m)
            if self.__analyzer.verify_same_person(p, photo):
                return True

        return False

    def try_save_new_photo(self, user: User, photo: Photo) -> PhotoMetadata | None:
        if not self.__is_user_present_on_photo(user, photo):
            return None
        analyzis_data = self.__analyzer.analyze(photo)
        # if not self.__is_expression_unique_for_user(user, analyzis_data):
        #     return None
        return self.__save_photo(user, photo, analyzis_data)

    def get_photo_count_for_user(self, user: User) -> int:
        return self.__metadata_repository.count_photos_for_user(user)

    def get_last_photos_for_user(self, user: User) -> list[Photo]:
        metadats = self.__metadata_repository.get_all_for_user_in_creation_order(user)
        photos = [self.__storage.get(m) for m in metadats]
        return photos

    def delete_last_photos_for_user(self, user: User):
        metadats = self.__metadata_repository.get_all_for_user_in_creation_order(user)
        for m in metadats:
            self.__storage.delete(m)

        self.__metadata_repository.delete_list(metadats)
