from typing import Tuple
from datetime import datetime
from uuid import uuid4

from backend.domain.photo.entity import AnalyzisData, Photo, PhotoMetadata
from backend.domain.user.entity import User


def create_base_dummies() -> Tuple[User, Photo, PhotoMetadata]:
    user = User(
        id=121,
        name="Dummy",
        profile_photo_path=None,
        verification_photo_metadata=None,
        balance=0,
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
