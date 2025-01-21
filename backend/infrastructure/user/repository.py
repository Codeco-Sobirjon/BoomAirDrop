from sqlalchemy import delete
from backend.domain.user.entity import User
from backend.domain.user.repository import IUserRepository
from backend.infrastructure.user.model import (
    UserModel,
)

from ..seedwork.repository import SqlAlchemyCrudRepository


class UserRepository(IUserRepository, SqlAlchemyCrudRepository[int, UserModel, User]):
    model_class = UserModel

    def delete(self, entity: User):
        raise NotImplementedError

    def get_all(self) -> list[User]:
        models = self._session.query(UserModel).all()
        return [self._object_mapper.to_obj(m) for m in models]
