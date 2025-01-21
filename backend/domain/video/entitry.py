from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from backend.domain.seedwork.entity import Entity
from backend.domain.user.entity import User


@dataclass
class VideoMetadata(Entity[UUID]):
    id: UUID
    user: User
    path: str
    publication_reward: int
    created_at: datetime
    published: bool = False
