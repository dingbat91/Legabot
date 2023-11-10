from discord.ext import commands
from discord import app_commands
import discord
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session
from legacydata.legacydata import FamilySheet, User
from misc.db import get_session


class familycommands(commands.Cog, name="family commands"):
    """A list of commands for managing a family"""

    def __init__(self, client: commands.Bot):
        self.client = client
        self._last_member = None

    @app_commands.command(
        name="add_family",
    )
    @app_commands.describe(name="Name of the family")
    @app_commands.describe(name="Description of the family")
    async def add_family(self, interaction: discord.Interaction, name: str):
        session = get_session()
        user = session.query(User).filter_by(discord_id=interaction.user.id).first()
        if not user:
            await interaction.response.send_message(
                f"{interaction.user.mention} you are not registered!", ephemeral=True
            )
            return

        family = FamilySheet(name=name)
        family.users.append(user)
        session.add(family)
        session.commit()
        session.close()
        await interaction.response.send_message(
            f"{interaction.user.mention}: Added family {name}", ephemeral=True
        )


async def setup(client: commands.Bot):
    await client.add_cog(familycommands(client))
