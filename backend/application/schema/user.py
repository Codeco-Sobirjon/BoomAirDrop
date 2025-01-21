from dataclasses import dataclass


@dataclass(frozen=True)
class UserResponceSchema:
    id: int
    name: str
    balance: float
