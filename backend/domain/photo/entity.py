from dataclasses import dataclass
from uuid import UUID
from backend.domain.seedwork.entity import Entity
from typing import TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from backend.domain.user.entity import User


type Photo = bytes


@dataclass(frozen=True)
class AnalyzisData:
    angry: float
    disgust: float
    fear: float
    happy: float
    sad: float
    surprise: float
    neutral: float


@dataclass
class PhotoMetadata(Entity[UUID]):
    user: "User"
    added: datetime
    extension: str
    analyzis_data: AnalyzisData
