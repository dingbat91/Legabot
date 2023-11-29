from discord.ext import commands
from discord import app_commands, Interaction, Embed
from discord.ui import Select, View
from legacydata.legacydata import FamilySheet
from misc.db import get_session, get_user, get_families
from misc.util import userMissing, familyMissing
from menu.family import familyMenu
import logging


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
        interaction: Interaction,
        name: str,
        reach: str,
        grasp: str,
        sleight: str,
    ):
        session = get_session()
        try:
            user = get_user(interaction.user.id, session=session)
        except Exception as e:
            await userMissing(interaction)
            return
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

        ## Check if family already exists
        try:
            families = get_families(user=user, session=session)
        except Exception as e:
            await familyMissing(interaction)
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

    ## select family to use
    @app_commands.command(
        name="select_family",
        description="Select a family to use",
    )
    async def select_family(self, interaction: Interaction):
        session = get_session()
        if session is False:
            await interaction.response.send_message(
                "The menu broke! (DB connection failed)",
                ephemeral=True,
                delete_after=20,
            )
            return
        try:
            user = get_user(interaction.user.id, session=session)
        ##No user exists in DB
        except Exception as e:
            await userMissing(interaction)
            return
        try:
            families = get_families(user=user, session=session)
        except Exception as e:
            await familyMissing(interaction)
            return
        ## If user has no families
        if len(families) == 0:
            await interaction.response.send_message(
                "You have no families!", ephemeral=True, delete_after=20
            )
            return
        ## If user only has one family
        if len(families) == 1:
            user.selected_family = families[0].id
            session.add(user)
            session.commit()
            await interaction.response.send_message(
                f"Selected {families[0].name} as your family!",
                ephemeral=True,
                delete_after=20,
            )
            session.close()
            return
        ## If user has multiple families
        ## Create select menu and options
        select = Select(placeholder="Select a family", min_values=1, max_values=1)
        for fam in families:
            select.add_option(label=fam.name, value=str(fam.id))

        ## close existing session
        session.close()

        ##? define callback
        async def select_callback(interaction: Interaction):
            session = get_session()
            if session is False:
                await interaction.response.send_message(
                    "The menu broke! (DB connection failed)",
                    ephemeral=True,
                    delete_after=20,
                )
                return
            user = get_user(interaction.user.id, session=session)
            ##No user exists in DB
            if user is None:
                await userMissing(interaction)
                return
            user.selected_family = int(select.values[0])
            families = get_families(user=user, session=session)
            ## If user not registered
            if families is False:
                return
            for f in families:
                if f.id == user.selected_family:
                    await interaction.response.send_message(
                        f"Selected {f.name} as your family!",
                        ephemeral=True,
                        delete_after=20,
                    )
                    session.add(user)
                    session.commit()
            session.close()

        ##? end callback definition
        select.callback = select_callback
        ## define view
        view = View()
        view.add_item(select)
        ## send message
        await interaction.response.send_message(
            "Select a family to use", ephemeral=True, view=view, delete_after=60
        )

    ## family Menu
    @app_commands.command(
        name="family_menu",
        description="Menu for managing your selected family",
    )
    async def family_menu(self, interaction: Interaction):
        view = familyMenu(interaction=interaction)
        await interaction.response.send_message(
            embed=view.createRootEmbed(), view=view, ephemeral=True, delete_after=500
        )


async def setup(client: commands.Bot):
    await client.add_cog(familycommands(client))
