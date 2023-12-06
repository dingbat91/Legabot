from typing import Any, Coroutine, Optional, Union
from discord.emoji import Emoji
from discord.partial_emoji import PartialEmoji
from discord.ui import Button, View, Modal, TextInput
from misc.db import sessionManager
from legacydata.legacydata import Family, User, FamilyMoves
from discord.utils import MISSING
from discord import Embed, Colour
from discord import Interaction, ButtonStyle, SelectOption
from sqlalchemy.orm import Session


##! Move List Classes
def createMovelistEmbed(family: Family):
    """Creates an embed for the move list"""
    embed = Embed(title=f"{family.name} Moves")
    for move in family.moves:
        embed.add_field(name=move.name, value=move.description, inline=False)
    return embed


class familyMoveList(View):
    session: sessionManager
    user: User
    family: Family
    create: Button

    def __init__(self, *, timeout: float | None = 180, discord_id: int):
        ## creation
        super().__init__(timeout=timeout)
        self.session = sessionManager()
        ## data loading
        s: Session
        user = self.session.getUser(discord_id)
        family = self.session.getSelectedFamily(user)
        button = createfamilyMove(row=0)
        self.add_item(button)


##! Move List Buttons
class createfamilyMove(Button):
    def __init__(
        self,
        *,
        style: ButtonStyle = ButtonStyle.secondary,
        label: str | None = "Create Move",
        disabled: bool = False,
        custom_id: str | None = None,
        url: str | None = None,
        emoji: str | Emoji | PartialEmoji | None = None,
        row: int | None = None,
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

    async def callback(self, interaction: Interaction) -> None:
        modal = createfamilyMoveModal(discord_id=interaction.user.id)
        await interaction.response.send_modal(modal)


class editfamilyMoves(Button):
    pass


class deletefamilyMove(Button):
    pass


##! Move List Selects


##! Move List Modals
class createfamilyMoveModal(Modal):
    name: TextInput = TextInput(
        label="Move Name",
        placeholder="Move Name",
        min_length=1,
        max_length=30,
        required=True,
        custom_id="name",
    )
    description: TextInput = TextInput(
        label="Move Description",
        placeholder="Move Description",
        min_length=1,
        max_length=2000,
        required=True,
        custom_id="description",
    )
    session: sessionManager = sessionManager()
    user: User
    family: Family

    def __init__(
        self,
        *,
        title: str = "Create Move",
        timeout: float | None = None,
        custom_id: str = MISSING,
        discord_id: int,
    ) -> None:
        super().__init__(title=title, timeout=timeout, custom_id=custom_id)
        with self.session as s:
            self.user = self.session.getUser(discord_id=discord_id)
            self.family = self.session.getSelectedFamily(self.user)

    def on_error(
        self, interaction: Interaction, error: Exception
    ) -> Coroutine[Any, Any, None]:
        return super().on_error(interaction, error)

    def on_timeout(self) -> Coroutine[Any, Any, None]:
        return super().on_timeout()

    async def on_submit(self, interaction: Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        new_move = FamilyMoves(name=self.name.value, description=self.description.value)
        s: Session
        with self.session as s:
            for moves in self.family.moves:
                if moves.name == new_move.name:
                    await interaction.followup.send(content="Move already exists")
                    return
            self.family.moves.append(new_move)
            s.add(self.family)
        embed = createMovelistEmbed(self.family)
        await interaction.edit_original_response(embed=embed)
