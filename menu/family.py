from typing import Any, Coroutine, Optional, Union, Literal
from discord import Interaction, Embed, ButtonStyle, SelectOption
from discord.emoji import Emoji
from discord.partial_emoji import PartialEmoji
from discord.ui import View, Button, button, Modal, TextInput, Select, select
from discord.ui.item import Item
from discord.utils import MISSING
from misc.db import sessionManager
from legacydata.legacydata import Family, User, FamilyMoves
import logging
from sqlalchemy.orm import Mapped, Session, joinedload
from menu.moves import familyMoveList, createMovelistEmbed


##! Select Family Classes
class selectFamilyBase(Select):
    session: sessionManager
    user: User

    def __init__(
        self, discordid: int, row: int | None = None, custom_id: str = MISSING
    ):
        """
        Allows a user to select a family from their list

        @discordid: The discord id of the user
        @row: The row to place the dropdown in
        """
        super().__init__(
            placeholder="Select a family",
            options=[],
            min_values=1,
            max_values=1,
            row=row,
            custom_id=custom_id,
        )
        self.session = sessionManager()
        with self.session as s:
            user = (
                s.query(User)
                .filter(User.discord_id == discordid)
                .options(joinedload(User.families))
                .first()
            )
            if user is None:
                raise ValueError("User not found")
            if len(user.families) == 0:
                self.disabled = True
                self.add_option(label="No families found", value="None")
                self.placeholder = "No families found"
            self.user = user
            for family in user.families:
                self.add_option(label=family.name, value=str(family.id))


class selectFamily(selectFamilyBase):
    def __init__(
        self, discordid: int, row: int | None = None, custom_id: str = "SelectFamily"
    ):
        super().__init__(discordid=discordid, row=row, custom_id=custom_id)

    async def callback(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        if self.disabled:
            return
        s: Session
        with self.session as s:
            self.user.selected_family = int(self.values[0])
            selectedfam = [
                fam for fam in self.user.families if fam.id == self.user.selected_family
            ][0]
            s.add(self.user)

        await interaction.edit_original_response(
            content=f"Selected family: **{selectedfam.name}**", view=None, embed=None
        )


## Delete Family Classes
class deleteFamily(selectFamilyBase):
    def __init__(
        self, discordid: int, row: int | None = None, custom_id: str = "DeleteFamily"
    ):
        super().__init__(discordid, row, custom_id=custom_id)

    async def callback(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        if self.disabled:
            return
        s: Session
        with self.session as s:
            selectedfam = [
                fam for fam in self.user.families if fam.id == int(self.values[0])
            ][0]
            if self.user.selected_family == selectedfam.id:
                self.user.selected_family = None
            s.delete(selectedfam)
        await interaction.edit_original_response(
            content=f"Deleted family: **{selectedfam.name}**", view=None, embed=None
        )


##! Family Main Menu Classes
def familyEmbed(family: Family) -> Embed:
    embed = Embed(title=f"Family: {family.name}")
    embed.add_field(
        name="Stats",
        value=f"**Sleight**: {family.sleight}\n**Grasp**: {family.grasp}\n**Reach**: {family.reach}",
    )
    embed.add_field(
        name="Resources",
        value=f"**Mood**: {family.mood}\n**Data**: {family.data}\n**Tech**: {family.tech}",
    )
    return embed


class familyMenu(View):
    """
    Core view for the family Menu
    """

    session = sessionManager()
    user: User
    family: Family
    __stats = ["sleight", "grasp", "reach"]
    __resources = ["mood", "data", "tech"]

    def __init__(self, discord_id: int, timeout: int | None = None):
        super().__init__(timeout=timeout)
        self.user = self.session.getUser(discord_id)
        if self.user.selected_family is None:
            raise ValueError("User has no selected family")
        with self.session as s:
            family = (
                s.query(Family).filter(Family.id == self.user.selected_family).first()
            )
            if family is None:
                raise ValueError("Family not found")
            self.family = family
        self.add_item(
            renameButton(
                label="Rename",
                session=self.session,
                family=self.family,
                style=ButtonStyle.secondary,
                custom_id="Rename",
            )
        )
        self.add_item(
            moveMenuButton(
                label="Moves",
                session=self.session,
                family=self.family,
                style=ButtonStyle.secondary,
                row=3,
            )
        )
        ## Iterates through the stats and resources and adds buttons for each
        for stat in self.__stats:
            self.add_item(
                statbutton(
                    label=f"{stat}+",
                    style=ButtonStyle.blurple,
                    family=self.family,
                    direction="up",
                    stat=stat,
                    row=1,
                    session=self.session,
                    custom_id=f"{stat}+",
                )
            )
            self.add_item(
                statbutton(
                    label=f"{stat}-",
                    style=ButtonStyle.red,
                    family=self.family,
                    direction="down",
                    stat=stat,
                    row=2,
                    session=self.session,
                    custom_id=f"{stat}-",
                )
            )

    def createEmbed(self) -> Embed:
        return familyEmbed(self.family)


##! Button Section
class statbutton(Button):
    """
    Button for changing a stat, used in the family menu
    """

    up: bool
    family: Family
    stat: str
    session: sessionManager

    def __init__(
        self,
        label: str,
        style: ButtonStyle,
        family: Family,
        direction: Literal["up"] | Literal["down"],
        stat: str,
        session: sessionManager,
        row: int | None = None,
        custom_id: str | None = None,
    ):
        super().__init__(label=label, style=style, row=row, custom_id=custom_id)
        if direction == "up":
            self.up = True
        else:
            self.up = False
        self.family = family
        self.stat = stat
        self.session = session

    async def callback(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        current_stat_value = getattr(self.family, self.stat)
        if self.up:
            setattr(self.family, self.stat, current_stat_value + 1)
        else:
            setattr(self.family, self.stat, current_stat_value - 1)
        with self.session as s:
            s.add(self.family)
        embed = familyEmbed(self.family)
        await interaction.edit_original_response(embed=embed)


class renameButton(Button):
    """
    Button to open the rename modal.
    """

    def __init__(
        self,
        *,
        style: ButtonStyle = ButtonStyle.secondary,
        label: str | None = "Rename",
        disabled: bool = False,
        custom_id: str | None = None,
        url: str | None = None,
        emoji: str | Emoji | PartialEmoji | None = None,
        row: int | None = None,
        session: sessionManager,
        family: Family,
    ):
        super().__init__(
            style=style,
            label=label,
            disabled=disabled,
            custom_id=custom_id,
            url=url,
            emoji=emoji,
            row=row,
        )
        self.session = session
        self.family = family

    async def callback(self, interaction: Interaction):
        modal = renameModal(
            title="Rename Family", session=self.session, family=self.family
        )
        await interaction.response.send_modal(modal)


class moveMenuButton(Button):
    family: Family
    session: sessionManager

    def __init__(
        self,
        *,
        style: ButtonStyle = ButtonStyle.secondary,
        label: str | None = None,
        disabled: bool = False,
        custom_id: str | None = None,
        url: str | None = None,
        emoji: str | Emoji | PartialEmoji | None = None,
        row: int | None = None,
        session: sessionManager,
        family: Family,
    ):
        super().__init__(
            style=style,
            label=label,
            disabled=disabled,
            custom_id=custom_id,
            url=url,
            emoji=emoji,
            row=row,
        )
        self.family = family
        self.session = session

    async def callback(self, interaction: Interaction):
        View = familyMoveList(discord_id=interaction.user.id)
        embed = createMovelistEmbed(family=self.family)
        await interaction.response.send_message(embed=embed, view=View, ephemeral=True)


##! Modal section
class renameModal(Modal):
    new_name: TextInput
    session: sessionManager
    family: Family

    def __init__(self, title: str, session: sessionManager, family: Family):
        super().__init__(timeout=120, title=title, custom_id="RenameModal")
        self.family = family
        self.session = session
        self.new_name = TextInput(
            label="Entry",
            placeholder="New Name",
            min_length=1,
            max_length=50,
        )
        self.add_item(self.new_name)

    async def on_submit(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        self.family.name = self.new_name.value
        with self.session as s:
            s.add(self.family)
        embed = familyEmbed(self.family)
        await interaction.edit_original_response(embed=embed)

    async def on_error(self, interaction: Interaction, error: Exception) -> None:
        await interaction.response.send_message(
            f"An error occured: {error}", ephemeral=True
        )
        logging.error(error)
        await super().on_error(interaction, error)

    async def on_timeout(self) -> None:
        return await super().on_timeout()
