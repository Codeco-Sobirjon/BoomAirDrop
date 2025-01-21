from abc import ABC, abstractmethod

from backend.domain.photo.entity import AnalyzisData, Photo, PhotoMetadata


class IPhotoAnalyzer(ABC):

    @abstractmethod
    def analyze(self, photo: Photo) -> AnalyzisData:
        raise NotImplementedError

    @abstractmethod
    def verify_same_person(self, photo1: Photo, photo2: Photo) -> bool:
        raise NotImplementedError


class IPhotoStorage(ABC):

    @abstractmethod
    def save(self, photo: Photo, photo_metadata: PhotoMetadata):
        raise NotImplementedError

    @abstractmethod
    def get(self, photo_metadata: PhotoMetadata) -> Photo:
        raise NotImplementedError

    @abstractmethod
    def delete(self, photo_metadata: PhotoMetadata):
        raise NotImplementedError


class IPhotoExtensionGuesser(ABC):
    @abstractmethod
    def guess(self, photo: Photo) -> str:
        raise NotImplementedError
