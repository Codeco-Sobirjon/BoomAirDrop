from abc import ABC, abstractmethod

from backend.domain.photo.entity import Photo
from backend.domain.user.entity import User

type Video = bytes


class IVideoCreator(ABC):
    @abstractmethod
    def create_video(self, photos: list[Photo], fps: int = 4) -> Video:
        raise NotImplementedError


class IVideoStorage(ABC):
    @abstractmethod
    def save_and_get_path(self, video: Video) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_by_path(self, path: str) -> Video:
        raise NotImplementedError


@abstractmethod
class IVideoPublisher(ABC):
    @abstractmethod
    def publish(self, video: Video, comment: str, user: User) -> None:
        raise NotImplementedError
