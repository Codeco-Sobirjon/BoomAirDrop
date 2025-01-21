from uuid import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped
from typing import Any, Protocol


class Base(DeclarativeBase):
    pass
