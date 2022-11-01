import sqlalchemy
import sqlalchemy.orm
import os

def _get_engine():
    usr = os.environ.get("DBUSER")
    pw = os.environ.get("DBPW")
    h = os.environ.get("DBHOST")
    dbname = os.environ.get("DBNAME")

    engine = sqlalchemy.create_engine(
        f"mysql+pymysql://{usr}:{pw}@{h}/{dbname}?charset=utf8mb4", echo=True)
    return engine

Base = sqlalchemy.orm.declarative_base(_get_engine())

class BaseQueryModel:
    @staticmethod
    def _load_session():
        metadata = Base.metadata
        Session = sqlalchemy.orm.sessionmaker(bind=_get_engine())
        session = Session()
        return session

    def __init__(self) -> None:
        self.session = BaseQueryModel._load_session()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()
