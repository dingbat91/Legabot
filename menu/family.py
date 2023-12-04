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
from sqlalchemy.orm import Mapped


##! Select Family Classes
class selectDropdown(Select):
    session: sessionManager = sessionManager()
    user: User
    options: list[SelectOption] = []

    def __init__(self, discordid: int, row: int | None = None):
        """
        Allows a user to select a family from their list

        @discordid: The discord id of the user
        @row: The row to place the dropdown in
        """
        with self.session as s:
            user = s.query(User).filter(User.discord_id == discordid).first()
            if user is None:
                raise ValueError("User not found")
            self.user = user
            for family in user.families:
                self.options.append(
                    SelectOption(label=family.name, value=str(family.id))
                )
            if len(self.options) == 0:
                self.disabled = True
                self.placeholder = "You have no families"
        super().__init__(
            placeholder="Select a family",
            options=self.options,
            max_values=1,
            min_values=1,
            row=row,
        )

    async def callback(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        if self.disabled:
            return
        with self.session as s:
            self.user.selected_family = int(self.values[0])
            selectedfam = [
                fam for fam in self.user.families if fam.id == self.user.selected_family
            ][0]
            s.add(self.user)
        await interaction.edit_original_response(
            content=f"Selected family: **{selectedfam.name}**", view=None, embed=None
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
        ## Iterates through the stats and resources and adds buttons for each
        for stat in self.__stats:
            self.add_item(
                statbutton(
                    label=f"{stat}+",
                    style=ButtonStyle.blurple,
                    family=self.family,
                    direction="up",
                    stat=stat,
                    row=0,
                    session=self.session,
                )
            )
            self.add_item(
                statbutton(
                    label=f"{stat}-",
                    style=ButtonStyle.red,
                    family=self.family,
                    direction="down",
                    stat=stat,
                    row=1,
                    session=self.session,
                )
            )

    def createEmbed(self) -> Embed:
        return familyEmbed(self.family)


class statbutton(Button):
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
    ):
        super().__init__(label=label, style=style, row=row)
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
