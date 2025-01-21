import httpx
from backend import config
from backend.domain.user.entity import User
from backend.domain.video.port import IVideoPublisher, Video


class TelegramDMVideoPublisher(IVideoPublisher):
    def publish(self, video: Video, comment: str, user: User) -> None:
        url = "https://api.telegram.org/bot" + config.BOT_TOKEN + "/sendVideo"
        thread_id = (
            config.RU_THREAD_ID if user.language == "ru" else config.EN_THREAD_ID
        )
        r = httpx.post(
            url,
            data={
                "chat_id": config.GROUP_ID,
                "message_thread_id": thread_id,
                "caption": comment,
            },
            files={"video": video},
        )
        assert r.status_code == 200
