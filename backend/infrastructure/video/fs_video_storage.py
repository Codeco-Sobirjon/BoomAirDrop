import os
from uuid import uuid4

from backend import config
from backend.domain.video.port import IVideoStorage, Video


class FSVideoStorage(IVideoStorage):
    def __init__(self):
        os.makedirs(config.VIDEOS_STORAGE_PATH, exist_ok=True)

    def save_and_get_path(self, video: Video) -> str:
        relative_path = str(uuid4()) + ".mp4"
        path = os.path.join(config.VIDEOS_STORAGE_PATH, relative_path)
        with open(path, "wb") as f:
            f.write(video)
        return relative_path

    def get_by_path(self, path: str) -> Video:
        full_path = os.path.join(config.VIDEOS_STORAGE_PATH, path)
        with open(full_path, "rb") as f:
            return f.read()
