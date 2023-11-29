from typing import Optional
from discord import Interaction, Webhook, Embed, ButtonStyle
from discord.ui import View, Button, button, Modal, TextInput
from discord.utils import MISSING
from sqlalchemy.orm import Session
from legacydata.legacydata import FamilySheet, User
from misc.db import get_session, get_user, get_families, get_family
from misc.util import userMissing, familyMissing
import logging


class familyMenu(View):
    session: Session
    __discord_id: int
    user: User
    family: FamilySheet

    def __init__(self, *, timeout: float | None = 500, interaction: Interaction):
        super().__init__(timeout=timeout)
        try:
            session = get_session()
        except Exception as e:
            logging.error(e)
            raise e
        self.session = session
        self.__discord_id = interaction.user.id
        self.user = get_user(self.__discord_id, session=self.session)
        self.family = get_family(interaction, session=self.session)

    def createRootEmbed(self):
        embed = Embed(title=f"{self.family.name} Family Menu")
        embed.add_field(name="Owner", value=f"{self.user.username}")
        embed.add_field(
            name="Stats",
            value=f"Reach: {self.family.reach}\nGrasp: {self.family.grasp}\nSleight: {self.family.sleight}",
        )
        embed.add_field(
            name="Resources",
            value=f"Data: {self.family.data},Tech: {self.family.tech},mood: {self.family.mood}",
        )
        return embed

    @button(label="Rename", style=ButtonStyle.blurple)
    async def rename(self, interaction: Interaction, button: Button):
        modal = renameModal(
            title=f"Rename {self.family.name}", custom_id=MISSING, view=self
        )
        await interaction.response.send_modal(modal)
        await modal.wait()
        logging.info("adjusting DB")
        self.session.add(self.family)
        self.session.commit()


class renameModal(Modal):
    name = TextInput(
        label="New Name",
        placeholder="Name",
        min_length=1,
        max_length=100,
        required=True,
    )
    view: familyMenu

    def __init__(
        self,
        *,
        title: str,
        timeout: float | None = None,
        custom_id: str = MISSING,
        view: familyMenu,
    ) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        self.view = view

    async def on_submit(self, interaction: Interaction) -> None:
        self.view.family.name = self.name.value
        embed = self.view.createRootEmbed()
        logging.info("loading embed")
        await interaction.response.edit_message(embed=self.view.createRootEmbed())
        return await super().on_submit(interaction)
