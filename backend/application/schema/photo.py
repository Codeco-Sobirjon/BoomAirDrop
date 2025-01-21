from dataclasses import dataclass


@dataclass(frozen=True)
class PhotoSubmissionResponse:
    success: bool
