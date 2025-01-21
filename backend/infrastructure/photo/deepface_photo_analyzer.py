from deepface import DeepFace
import cv2
import numpy as np

from backend.domain.photo.entity import Photo, AnalyzisData
from backend.domain.photo.port import IPhotoAnalyzer
import backend.config as cfg

# Preload the model for verification (optional, as DeepFace handles this internally).
DeepFace.build_model(model_name=cfg.PHOTO_ANALYZIS_MODEL)


class DeepfacePhotoAnalyzer(IPhotoAnalyzer):
    @staticmethod
    def __to_internal_format(photo: Photo):
        bts = np.asarray(bytearray(photo), dtype=np.uint8)
        img = cv2.imdecode(bts, cv2.IMREAD_COLOR)
        return np.asarray(img)

    def verify_same_person(self, photo1: Photo, photo2: Photo) -> bool:
        im1 = self.__to_internal_format(photo1)
        im2 = self.__to_internal_format(photo2)

        res = DeepFace.verify(
            im1,
            im2,
            model_name=cfg.PHOTO_ANALYZIS_MODEL,
            enforce_detection=False,
        )
        return res["verified"]

    def analyze(self, photo: Photo) -> AnalyzisData:
        im = self.__to_internal_format(photo)
        # Perform emotion analysis
        emotions = DeepFace.analyze(im, actions=["emotion"], enforce_detection=False)[0]["emotion"]
        return AnalyzisData(**emotions)
