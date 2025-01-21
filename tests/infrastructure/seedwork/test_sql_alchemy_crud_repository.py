from dataclasses import dataclass
import unittest

from sqlalchemy.orm import Mapped, mapped_column

from backend.infrastructure.seedwork.mapper import IObjectMapper
from backend.infrastructure.seedwork.model import Base, BaseModel
from backend.infrastructure.seedwork.repository import SqlAlchemyCrudRepository
from .posrgres_session_mixin import PostgresSessionMixin
from backend.domain.seedwork.entity import Entity


@dataclass
class ExampleEntity(Entity[int]):
    name: str


class ExampleModel(Base):
    __tablename__ = "example"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class ExampleObjectMapper(IObjectMapper[ExampleEntity, ExampleModel]):
    def to_obj(self, obj: ExampleModel) -> ExampleEntity:
        return ExampleEntity(id=obj.id, name=obj.name)

    def from_obj(self, obj: ExampleEntity) -> ExampleModel:
        return ExampleModel(id=obj.id, name=obj.name)


class ExampleRepository(SqlAlchemyCrudRepository[int, ExampleModel, ExampleEntity]):
    model_class = ExampleModel


mapper = ExampleObjectMapper()


class TestSqlAlchemyCrudRepository(PostgresSessionMixin, unittest.TestCase):
    model_class = ExampleModel

    def test_create(self):
        # Given
        repo = ExampleRepository(self.session, mapper)
        example = ExampleEntity(id=1, name="example")

        # When
        repo.create(example)
        self.session.commit()

        # Then
        saved = self.session.get(ExampleModel, example.id)
        assert saved is not None
        saved_entity = mapper.to_obj(saved)
        self.assertEqual(example, saved_entity)

    def test_update(self):
        # Given
        repo = ExampleRepository(self.session, mapper)
        example = ExampleEntity(id=1, name="example")
        repo.create(example)
        self.session.commit()

        # When
        example.name = "example updated"
        repo.update(example)
        self.session.commit()

        # Then
        saved = self.session.get(ExampleModel, example.id)
        assert saved is not None
        saved_entity = mapper.to_obj(saved)
        self.assertEqual(example, saved_entity)

    def test_delete(self):
        # Given
        repo = ExampleRepository(self.session, mapper)
        example = ExampleEntity(id=1, name="example")
        repo.create(example)
        self.session.commit()

        # When
        repo.delete(example)
        self.session.commit()

        # Then
        saved = self.session.get(ExampleModel, example.id)
        self.assertIsNone(saved)

    def test_get_by_id(self):
        # Given
        repo = ExampleRepository(self.session, mapper)
        example = ExampleEntity(id=1, name="example")
        repo.create(example)
        self.session.commit()

        # When
        saved = repo.get_by_id(1)

        # Then
        self.assertEqual(example, saved)

    def test_get_by_id_not_found(self):
        # Given
        repo = ExampleRepository(self.session, mapper)

        # When
        saved = repo.get_by_id(1)

        # Then
        self.assertIsNone(saved)


if __name__ == "__main__":
    unittest.main()
