from dataclasses import dataclass
from backend.domain.seedwork.entity import Entity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.domain.photo.entity import PhotoMetadata


@dataclass
class User(Entity[int]):
    name: str
    profile_photo_path: str | None
    verification_photo_metadata: "PhotoMetadata | None"
    balance: int
    is_premium: bool
    language: str

