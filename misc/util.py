from discord import Interaction


async def userMissing(interaction: Interaction):
    await interaction.response.send_message(
        "You are not registered!", ephemeral=True, delete_after=20
    )
    return


async def familyMissing(interaction: Interaction):
    await interaction.response.send_message(
        "You do not have a family selected", ephemeral=True, delete_after=20
    )
    return
