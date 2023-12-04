from discord.ext import commands
from discord import app_commands
import discord
from legacydata.legacydata import Family, User
from misc.db import sessionManager


class usercommands(commands.GroupCog, group_name="user"):
    """commands for managing and registering a user"""

    def __init__(self, client: commands.Bot):
        self.client = client
        self._last_member = None

    @app_commands.commands.command(name="register", description="Registers a user")
    async def register(
        self,
        interaction: discord.Interaction,
    ):
        session = sessionManager()
        with session as s:
            user = s.query(User).filter(User.discord_id == interaction.user.id).first()
            if user is None:
                user = User(
                    discord_id=interaction.user.id, username=interaction.user.name
                )
                s.add(user)
                await interaction.response.send_message(
                    "User registered", ephemeral=True, delete_after=10
                )
            else:
                await interaction.response.send_message(
                    "User already registered", ephemeral=True, delete_after=10
                )


async def setup(client: commands.Bot):
    await client.add_cog(usercommands(client))
