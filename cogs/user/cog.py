from discord.ext import commands
from discord import app_commands
import discord
from legacydata.legacydata import FamilySheet, User
from misc.db import get_session, get_user


class usercommands(commands.Cog, name="user commands"):
    """commands for managing and registering a user"""

    def __init__(self, client: commands.Bot):
        self.client = client
        self._last_member = None

    @app_commands.command(
        name="register_user", description="Registers a new user to the system"
    )
    async def setupUser(self, interaction: discord.Interaction):
        session = get_session()
        user = await get_user(interaction, session=session)
        if user is not None:
            await interaction.response.send_message(
                "You are already registered", ephemeral=True
            )
            return
        # Creates user is one doesn't exist
        session = get_session()
        user = User(username=interaction.user.name, discord_id=interaction.user.id)
        session.add(user)
        session.commit()
        session.close()
        await interaction.response.send_message(
            f"Registered {interaction.user.name}", ephemeral=True, delete_after=10
        )


async def setup(client: commands.Bot):
    await client.add_cog(usercommands(client))
