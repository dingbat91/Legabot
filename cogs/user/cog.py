from discord.ext import commands
from discord import app_commands
import discord
from legacydata.legacydata import FamilySheet, User
from misc.db import get_session


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
        existing_user = (
            session.query(User).filter_by(discord_id=interaction.user.id).first()
        )
        if existing_user:
            print("user already exists")
            await interaction.response.send_message(
                f"{interaction.user.mention} your already registered!",
                ephemeral=True,
            )
            return
        else:
            user = User(username=interaction.user.name, discord_id=interaction.user.id)
            session.add(user)
            session.commit()
            existing_user = (
                session.query(User).filter_by(discord_id=interaction.user.id).first()
            )
            print("added user")
        session.close()
        if existing_user:
            await interaction.response.send_message(
                f"{interaction.user.mention}: Registered user {existing_user.username}",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                f"Failed to register user {interaction.user.name}", ephemeral=True
            )


async def setup(client: commands.Bot):
    await client.add_cog(usercommands(client))
