from discord.ext import commands
from discord import app_commands, SelectOption
from discord.ui import Select, View
import discord
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session, joinedload
from legacydata.legacydata import FamilySheet, User
from misc.db import get_session, get_user, get_families


class familycommands(commands.Cog, name="family commands"):
    """A list of commands for managing a family"""

    def __init__(self, client: commands.Bot):
        self.client = client
        self._last_member = None

    ##adds family (With it's starting reach,grasp, and sleight) to DB and links it to the user.
    @app_commands.command(
        name="add_family",
        description="Adds a family to your ID",
    )
    @app_commands.describe(name="Name of the family")
    @app_commands.describe(reach="Reach of the family")
    @app_commands.describe(grasp="Grasp of the family")
    @app_commands.describe(sleight="Sleight of the family")
    async def add_family(
        self,
        interaction: discord.Interaction,
        name: str,
        reach: str,
        grasp: str,
        sleight: str,
    ):
        session = get_session()
        ## Family Sheet creation
        if not (reach.isdigit() and grasp.isdigit() and sleight.isdigit()):
            await interaction.response.send_message(
                "Reach, Grasp, and Sleight must be numbers",
                ephemeral=True,
                delete_after=20,
            )
            return
        intReach = int(reach)
        intGrasp = int(grasp)
        intSleight = int(sleight)
        family = FamilySheet(
            name=name, reach=intReach, grasp=intGrasp, sleight=intSleight
        )
        user = await get_user(interaction, session=session)
        ##No user exists in DB
        if user is None:
            await interaction.response.send_message(
                "You are not registered!", ephemeral=True, delete_after=20
            )
            return

        ## Check if family already exists
        families = await get_families(
            user=user, interaction=interaction, session=session
        )
        if families is False:
            return

        for fam in families:
            if fam.name == name:
                await interaction.response.send_message(
                    "Family already exists!", ephemeral=True, delete_after=20
                )
                return

        ## Add family to user
        user.families.append(family)
        session.add(user)
        session.commit()
        session.close()
        await interaction.response.send_message(
            f"Added {name} to your families!", ephemeral=True, delete_after=20
        )


async def setup(client: commands.Bot):
    await client.add_cog(familycommands(client))
