from fastapi import FastAPI
from ratelimit import RateLimitMiddleware, Rule
from ratelimit.auths import EmptyInformation
from ratelimit.backends.simple import MemoryBackend
from ratelimit.types import Scope
from typing_extensions import Tuple
from urllib.parse import parse_qsl
from backend.application.authorization.tg_miniapp_init_authorization import InitDataUser
from backend.application.routers import base

app = FastAPI()


# Custom authentication function
async def AUTH_FUNCTION(scope: Scope) -> Tuple[str, str]:
    for name, value in scope["headers"]:
        if b"init-data" == name:
            init_data = dict(parse_qsl(value))
            user = InitDataUser.model_validate_json(init_data[b"user"])
            user_id = user.id
            break
    else:
        user_id = None

    if user_id is None:
        raise EmptyInformation(scope)

    return str(user_id), "default"


# Rate limit middleware with custom authentication
app.add_middleware(
    RateLimitMiddleware,
    authenticate=AUTH_FUNCTION,
    backend=MemoryBackend(),
    config={r"^/api/photos/submit": [Rule(minute=15, second=1, block_time=4)]},
)

# Include the API router
app.include_router(base.router, prefix="/api")
