from pydantic import BaseModel
from dataclasses import dataclass


@dataclass(frozen=True)
class ReferalStats(BaseModel):
    premium_count: int
    basic_count: int
    earned_tokens: float


@dataclass(frozen=True)
class ReferalSchema(BaseModel):
    id: int
    name: str
    earned: float
