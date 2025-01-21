import unittest
from backend.infrastructure.photo.mapper import PhotoMetadataModelMapper
from backend.infrastructure.photo.model import PhotoMetadataModel
from backend.infrastructure.photo.repository import PhotoMetadataRepository
from backend.infrastructure.user.mapper import UserModelMapper
from backend.infrastructure.user.model import (
    UserModel,
)
from backend.infrastructure.user.repository import UserRepository
from ...domain.test_user_service import create_dummies
from tests.infrastructure.seedwork.posrgres_session_mixin import PostgresSessionMixin


photo_mapper = PhotoMetadataModelMapper()
user_mapper = UserModelMapper(photo_mapper)


class TestUserSave(PostgresSessionMixin, unittest.TestCase):
    model_class = PhotoMetadataModel

    def test_save(self):
        UserModel.metadata.create_all(self.engine)
        user_repo = UserRepository(self.session, user_mapper)
        photo_repo = PhotoMetadataRepository(self.session, photo_mapper)

        (user, _, photo_meta) = create_dummies()
        user.verification_photo_metadata = None

        user_repo.create(user)
        photo_repo.create(photo_meta)
        user.verification_photo_metadata = photo_meta
        user_repo.update(user)

        self.session.commit()

        u = user_repo.get_by_id(user.id)
        assert u is not None
        self.assertIsNotNone(u.verification_photo_metadata)

        user.verification_photo_metadata = None
        user_repo.update(user)
        self.session.commit()


if __name__ == "__main__":
    unittest.main()
