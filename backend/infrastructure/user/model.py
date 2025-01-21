from uuid import UUID
from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Integer

from ..seedwork.model import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..photo.model import PhotoMetadataModel


class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str]
    balance: Mapped[int] = mapped_column(BigInteger)
    verification_photo_metadata_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("photo_metadata.id")
    )
    verification_photo_metadata: Mapped["PhotoMetadataModel | None"] = relationship(
        "PhotoMetadataModel",
        foreign_keys=[verification_photo_metadata_id],
        viewonly=True,
        cascade="",
    )
    profile_photo_path: Mapped[str | None]
    is_premium: Mapped[bool]
    language: Mapped[str]

    def __init__(
        self,
        id: int,
        name: str,
        profile_photo_path: str | None,
        balance: int,
        verification_photo_metadata_id: UUID | None,
        is_premium: bool,
        language: str,
    ):
        self.id = id
        self.name = name
        self.profile_photo_path = profile_photo_path
        self.balance = balance
        self.verification_photo_metadata_id = verification_photo_metadata_id
        self.is_premium = is_premium
        self.language = language
