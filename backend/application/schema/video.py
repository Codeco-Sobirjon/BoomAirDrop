from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class VideoSchema(BaseModel):
    id: UUID
    playback_url: str
    reward: float
    created_at: datetime
    published: bool


class VideoResponseSchema(BaseModel):
    total: int
    videos: list


class VideoPublisRequest(BaseModel):
    id: UUID
    comment: str
