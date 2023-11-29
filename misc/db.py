from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session, Session, joinedload
from legacydata.legacydata import base, FamilySheet, User
from discord import app_commands
from discord import Interaction
from discord.ext import commands
from misc.util import userMissing, familyMissing
import logging


def get_session():
    engine = create_engine("postgresql://sqlalch:pass@localhost:5432/Legacy")
    base.metadata.create_all(engine)
    try:
        session = sessionmaker(bind=engine)
        return session()
    except Exception as e:
        logging.error(e)
        raise e


##Gets User from DB Via Discord ID
## Does not return a message if user doesn't exist. Should be handled by the command as this may be called creating a user.
def get_user(id: int, session: Session):
    session = session
    user = session.query(User).filter_by(discord_id=id).first()
    if user is None:
        raise Exception("User is not registered")
    return user


##Gets Family from DB Via User ID
## Does not check if any families exists. Should be handled by the command as this may be called creating a family.
def get_families(user: User, session: Session):
    return user.families


def get_family(interaction: Interaction, session: Session):
    user = get_user(interaction.user.id, session=session)
    if user is None:
        raise Exception("User is not registered")
    family = session.query(FamilySheet).filter_by(id=user.selected_family).first()
    if family is None:
        raise Exception("User does not have a family selected")
    return family
