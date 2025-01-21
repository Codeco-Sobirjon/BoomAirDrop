from backend.domain.seedwork.entity import Entity
from backend.domain.seedwork.repository import ICrudRepository
from backend.infrastructure.seedwork.mapper import IObjectMapper
from backend.infrastructure.seedwork.model import Base
from sqlalchemy.orm import Session
from typing import TypeVar, Generic

M = TypeVar("M", bound=Base)
ID = TypeVar("ID")
E = TypeVar("E", bound=Entity)


class SqlAlchemyCrudRepository(Generic[ID, M, E], ICrudRepository[ID, E]):
    model_class: type[M]

    def __init__(self, session: Session, object_mapper: IObjectMapper[E, M]):
        self._session = session
        self._object_mapper = object_mapper

    def get_by_id(self, id: ID) -> E | None:
        res = self._session.get(self.model_class, id)
        return None if res is None else self._object_mapper.to_obj(res)

    def create(self, entity: E):
        model = self._object_mapper.from_obj(entity)
        self._session.add(model)
        self._session.flush()

    def update(self, entity: E):
        model = self._object_mapper.from_obj(entity)
        self._session.merge(model)
        self._session.flush()
