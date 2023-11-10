from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session
from legacydata.legacydata import base


def get_session():
    engine = create_engine("postgresql://sqlalch:pass@localhost:5432/Legacy")
    base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    return session()
