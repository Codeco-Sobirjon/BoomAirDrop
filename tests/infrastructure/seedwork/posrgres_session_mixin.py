import sqlalchemy
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from backend.infrastructure.seedwork.model import Base, BaseModel

_pg = PostgresContainer("postgres:16-alpine")


class PostgresSessionMixin[E: Base]:
    model_class: type[E]

    @classmethod
    def setUpClass(cls):
        _pg.start()
        pg_url = _pg.get_connection_url().replace("psycopg2", "psycopg")
        cls.engine = sqlalchemy.create_engine(pg_url, pool_pre_ping=True, echo=True)
        cls.model_class.metadata.create_all(cls.engine)
        cls.SessionMaker = sessionmaker(bind=cls.engine, expire_on_commit=False)

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()
        _pg.stop()

    def setUp(self):
        self.session = self.SessionMaker()

    def tearDown(self):
        self.session.query(self.model_class).delete()
        self.session.commit()
        self.session.close()
