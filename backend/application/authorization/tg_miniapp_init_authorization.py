import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Annotated
from urllib.parse import parse_qsl

from fastapi import Header, HTTPException, status
from pydantic import BaseModel
import backend.config as conf
import backend.constants as const


class InitDataUser(BaseModel):
    id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    photo_url: str | None = None
    is_premium: bool | None = None
    language_code: str | None = None
    start_param: str | None = None

    def get_full_name(self) -> str:
        full_name = self.first_name
        if self.last_name and len(self.last_name) > 0:
            full_name += " " + self.last_name

        return full_name


def is_data_geniune(fields: dict) -> bool:
    hash = fields.pop("hash")
    kvs = sorted(fields.items(), key=lambda x: x[0])
    parts = [f"{k}={v}" for k, v in kvs]
    data_check_str = "\n".join(parts)
    data_check = hmac.new(
        conf.HMAC_VALIDATION_SECRET_KEY, data_check_str.encode(), hashlib.sha256
    )
    return data_check.hexdigest() == hash


def is_data_expired(fields: dict) -> bool:
    auth_date = datetime.fromtimestamp(int(fields["auth_date"]))
    delta: timedelta = datetime.now() - auth_date
    return delta.days > const.INIT_DATA_EXPIRE_HOURS


def tg_miniapp_header_init_authorization(
    init_data: Annotated[str | None, Header()]
) -> InitDataUser:
    if init_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No Init-Data header provided",
        )

    fields = dict(parse_qsl(init_data))

    if not is_data_geniune(fields):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Init-Data header",
        )

    if is_data_expired(fields):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Init-Data expired",
        )

    user = InitDataUser.model_validate_json(fields["user"])
    user.start_param = fields.get("start_param")
    return user
