from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.item import Base


def init_db(uri):
    engine = create_engine(uri)
    db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)
    return db_session
