from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session, joinedload
from legacydata.legacydata import base, Family, User
from discord import Interaction
import logging


## Class for building sessions
class sessionBuilder:
    engine: Engine
    maker: sessionmaker
    session: Session

    def __init__(self, url: str = "postgresql://sqlalch:pass@localhost:5432/Legacy"):
        self.engine = create_engine(
            url, echo=False
        )  # set echo to True to see SQL queries
        self.maker = sessionmaker(bind=self.engine)

    ## creates the tables in the database if they do not exist
    def initialiseDB(self):
        try:
            base.metadata.create_all(self.engine)
        except Exception as e:
            logging.error(e)
            raise e

    def create_session(self):
        return self.maker()


## Class for managing a session
class sessionManager:
    builder = sessionBuilder()
    session: Session

    def __init__(self):
        self.session = self.builder.create_session()

    ## when deleted, closes the session
    def __del__(self):
        self.session.close()

    def getUser(self, discord_id: int):
        """Gets a user from the DB"""
        try:
            user = (
                self.session.query(User).filter(User.discord_id == discord_id).first()
            )
            if user is None:
                raise ValueError("User not found")
            return user
        except Exception as e:
            logging.error(e)
            raise e

    def getSelectedFamily(self, user: User):
        """Gets a users selected family from the DB"""
        try:
            if user.selected_family is None:
                raise ValueError("No family selected")
            family = (
                self.session.query(Family)
                .filter(Family.id == user.selected_family)
                .first()
            )
            if family is None:
                raise ValueError("Family not found")
            return family
        except Exception as e:
            logging.error(e)
            raise e

    ## when entered as a context manager, returns the session
    def __enter__(self):
        """Returns the session for use in a context manager"""
        return self.session

    ## when exited as a context manager, commits the session, rolls back if an error is raised
    def __exit__(self, exc_type, exc_value, traceback):
        """Commits the session, rolls back if an error is raised"""
        if exc_type is not None:
            self.session.rollback()
            logging.error(exc_value)
            raise exc_value
        else:
            self.session.commit()
