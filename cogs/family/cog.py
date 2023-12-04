from discord.ext import commands
from discord import app_commands, Interaction, Embed
from discord.ui import Select, View
from legacydata.legacydata import Family, User
from misc.db import sessionManager
from menu.family import selectDropdown, familyMenu
import logging


class familycommands(commands.GroupCog, group_name="family"):

    """A list of commands for managing a family"""

    def __init__(self, client: commands.Bot):
        self.client = client
        self._last_member = None

    @app_commands.describe(name="Name of the namily to create")
    @app_commands.command(name="create", description="Creates a family")
    async def create_family(self, interaction: Interaction, name: str):
        session = sessionManager()
        try:
            user = session.getUser(interaction.user.id)
        except Exception as e:
            logging.error(e)
            await interaction.response.send_message(
                f"An error occured. Error:{e}", ephemeral=True, delete_after=20
            )
            return
        with session as s:
            for family in user.families:
                if family.name == name:
                    await interaction.response.send_message(
                        "Family already exists", ephemeral=True
                    )
                    return
            family = Family(name=name)
            user.families.append(family)
            s.add(user)
            await interaction.response.send_message(
                f"Family {name} created", ephemeral=True, delete_after=20
            )

    @app_commands.command(name="select", description="Selects a family to manage")
    async def selectFamily(self, interaction: Interaction):
        view = View()
        view.add_item(selectDropdown(interaction.user.id))
        await interaction.response.send_message(
            content="Select a family", ephemeral=True, view=view
        )

    @app_commands.command(name="menu", description="Opens the family menu")
    async def menu(self, interaction: Interaction):
        view = familyMenu(interaction.user.id)
        embed = view.createEmbed()
        await interaction.response.send_message(
            content="Family Menu",
            ephemeral=True,
            embed=embed,
            view=view,
            delete_after=120,
        )


async def setup(client: commands.Bot):
    await client.add_cog(familycommands(client))
