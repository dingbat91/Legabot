from discord.ext import commands
from discord import app_commands
import discord
import os
import logging


class testcommands(commands.Cog, name="Test Commands"):
    """A list of commands for testing the bot"""

    def __init__(self, client: commands.Bot):
        self.client = client
        self._last_member = None

    @app_commands.command(name="hello")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"hello {interaction.user.mention}", ephemeral=True
        )

    @commands.is_owner()
    @app_commands.command(name="reload", description="Reloads all bogs")
    async def reload(
        self,
        interaction: discord.Interaction,
    ):
        for folder in os.listdir("cogs"):
            if os.path.exists(os.path.join("cogs", folder, "cog.py")):
                logging.info(f"Reloading {folder} cog")
                await self.client.reload_extension(f"cogs.{folder}.cog")
        embed = discord.Embed(
            title="Reload",
            description="Extensions successfully reloaded",
            color=0xFF00C8,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(client: commands.Bot):
    await client.add_cog(testcommands(client))
