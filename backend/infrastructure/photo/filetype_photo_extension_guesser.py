from filetype import filetype

from backend.domain.photo.entity import Photo
from backend.domain.photo.port import IPhotoExtensionGuesser


class FiletypePhotoExtensionGuesser(IPhotoExtensionGuesser):
    def guess(self, photo: Photo) -> str:
        ft = filetype.guess(photo)
        assert ft is not None, "Unknow photo format"
        return ft.extension
