from typing import Final
import os
import hmac
import hashlib


PHOTO_STORAGE_PATH: Final = os.getenv("PHOTO_STORAGE_PATH", "photos")
PHOTO_PROFILE_STORAGE_PATH: Final = os.path.join(PHOTO_STORAGE_PATH, "profile")
PHOTO_ANALYZIS_MODEL: Final = os.getenv("PHOTO_ANALYZIS_MODEL", "Facenet")

DB_DSN: Final = "postgresql://postgres:1111@localhost:5432/test"
#     os.getenv(
#     "DB_DSN", "postgresql+psycopg://postgres:1111@localhost:5432/test"
# ))

BOT_TOKEN: Final = os.getenv(
    "BOT_TOKEN", "902781892:AAF0HveNpkqup-cV8kurvCR5lWuIpi84rJE"
)

C_STR: Final = "WebAppData"

HMAC_VALIDATION_SECRET_KEY: Final = hmac.new(
    C_STR.encode(), BOT_TOKEN.encode(), hashlib.sha256
).digest()


APP_URL: Final = os.getenv("APP_URL", "https://t.me/DoomEternalBot/start")

VIDEOS_STORAGE_PATH: Final = os.getenv("VIDEOS_STORAGE_PATH", "videos")

GROUP_ID: Final = int(os.getenv("GROUP_ID", "-1002169893152"))
RU_THREAD_ID: Final = int(os.getenv("RU_THREAD_ID", "1"))
EN_THREAD_ID: Final = int(os.getenv("EN_THREAD_ID", "4"))
