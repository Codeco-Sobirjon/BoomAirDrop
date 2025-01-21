from backend.application.schema.user import UserResponceSchema
from backend.domain.user.entity import User
from backend.infrastructure.seedwork.mapper import IObjectMapper
import backend.constants as const


class UserSchemaMapper(IObjectMapper[User, UserResponceSchema]):
    def from_obj(self, obj: User) -> UserResponceSchema:
        return UserResponceSchema(
            id=obj.id,
            name=obj.name,
            balance=obj.balance / const.USER_BALANCE_PRECISION,
        )

    def to_obj(self, obj: UserResponceSchema) -> User:
        raise NotImplementedError
