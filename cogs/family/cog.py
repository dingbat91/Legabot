from discord.ext import commands
from discord import app_commands
import discord
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session
from legacydata.legacydata import FamilySheet


class testcommands(commands.Cog, name="family commands"):
    """A list of commands for managing a family"""

    def __init__(self, client: commands.Bot):
        self.client = client
        self._last_member = None

    def __get_session(self):
        engine = create_engine("postgresql://sqlalch:pass@localhost:5432/Legacy")
        session = sessionmaker(bind=engine)
        return session()

    @app_commands.command(
        name="add_family",
    )
    @app_commands.describe(name="Name of the family")
    @app_commands.describe(name="Description of the family")
    async def add_family(
        self, interaction: discord.Interaction, name: str, description: str
    ):
        family = FamilySheet(name=name, description=description)
        print(family)


async def setup(client: commands.Bot):
    await client.add_cog(testcommands(client))
