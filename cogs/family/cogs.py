from discord.ext import commands
from discord import app_commands
import discord
from ...Data.family.familysheet import FamilySheet


class testcommands(commands.Cog, name="family commands"):
    """A list of commands for managing a family"""

    def __init__(self, client: commands.Bot):
        self.client = client
        self._last_member = None

    """
    @app_commands.command(name="add_family")
    async def add_family(self, interaction: discord.Interaction,name: str):
        newfamily = FamilySheet(name=name, owner=interaction.user.id, reach=0, grasp=0, sleight=0)
    """


async def setup(client: commands.Bot):
    await client.add_cog(testcommands(client))
