from datetime import datetime
from uuid import UUID

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.properties import ForeignKey

from backend.infrastructure.seedwork.model import Base
from backend.infrastructure.user.model import UserModel


class VideoMetadataModel(Base):
    __tablename__ = "video_metadata"
    id: Mapped[UUID] = mapped_column(unique=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    user: Mapped[UserModel] = relationship(
        UserModel, viewonly=True, cascade="", foreign_keys=[user_id]
    )
    path: Mapped[str]
    publication_reward: Mapped[int]
    created_at: Mapped[datetime]
    published: Mapped[bool]

    def __init__(
        self,
        id: UUID,
        user_id: int,
        path: str,
        publication_reward: int,
        created_at: datetime,
        published: bool,
    ):
        self.id = id
        self.user_id = user_id
        self.path = path
        self.publication_reward = publication_reward
        self.created_at = created_at
        self.published = published
