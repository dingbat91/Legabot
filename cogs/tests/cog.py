from discord.ext import commands
from discord import app_commands
import discord


class testcommands(commands.Cog, name="Test Commands"):
    """A list of commands for testing the bot"""

    def __init__(self, client: commands.Bot):
        self.client = client
        self._last_member = None

    @app_commands.command(name="hello")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("hello")


async def setup(client: commands.Bot):
    await client.add_cog(testcommands(client))
