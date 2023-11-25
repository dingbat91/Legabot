from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session, Session, joinedload
from legacydata.legacydata import base, FamilySheet, User
from discord import app_commands
from discord import Interaction
from discord.ext import commands


def get_session():
    engine = create_engine("postgresql://sqlalch:pass@localhost:5432/Legacy")
    base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)
    return session()


##Gets User from DB Via Discord ID
## Does not return a message if user doesn't exist. Should be handled by the command as this may be called creating a user.
async def get_user(interaction: Interaction, session: Session):
    session = session
    user = session.query(User).filter_by(discord_id=interaction.user.id).first()
    return user


##Gets Family from DB Via User ID
## Does not check if any families exists. Should be handled by the command as this may be called creating a family.
async def get_families(user: User, interaction: Interaction, session: Session):
    if user is None:
        await interaction.response.send_message(
            "You are not registered", ephemeral=True, delete_after=30
        )
        return False
    return user.families


async def get_family(interaction: Interaction, session: Session):
    pass
