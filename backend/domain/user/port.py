from abc import ABC, abstractmethod


class IProfilePhotoDownloader(ABC):
    @abstractmethod
    def try_download_and_get_path(self, user_id: int) -> str | None:
        raise NotImplementedError
