from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, backref, relationship, mapped_column
from backend.infrastructure.seedwork.model import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..user.model import UserModel


class PhotoMetadataModel(Base):
    __tablename__ = "photo_metadata"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    added: Mapped[datetime]
    extension: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserModel"] = relationship(
        "UserModel",
        foreign_keys=[user_id],
        viewonly=True,
        backref=backref("users", cascade="all, delete-orphan"),
    )

    analyzis_data__angry: Mapped[float]
    analyzis_data__disgust: Mapped[float]
    analyzis_data__fear: Mapped[float]
    analyzis_data__happy: Mapped[float]
    analyzis_data__neutral: Mapped[float]
    analyzis_data__sad: Mapped[float]
    analyzis_data__surprise: Mapped[float]

    def __init__(
        self,
        id: UUID,
        added: datetime,
        extension: str,
        user_id: int,
        analyzis_data__disgust: float,
        analyzis_data__fear: float,
        analyzis_data__happy: float,
        analyzis_data__neutral: float,
        analyzis_data__sad: float,
        analyzis_data__surprise: float,
        analyzis_data__angry: float,
    ):
        self.id = id
        self.added = added
        self.extension = extension
        self.user_id = user_id
        self.analyzis_data__disgust = analyzis_data__disgust
        self.analyzis_data__fear = analyzis_data__fear
        self.analyzis_data__sad = analyzis_data__sad
        self.analyzis_data__angry = analyzis_data__angry
        self.analyzis_data__happy = analyzis_data__happy
        self.analyzis_data__neutral = analyzis_data__neutral
        self.analyzis_data__surprise = analyzis_data__surprise
