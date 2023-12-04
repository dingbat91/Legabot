import discord
from discord.ext import commands
from dotenv import load_dotenv
from sqlalchemy.orm import close_all_sessions
from misc.db import sessionBuilder
import os
import logging
import typing
import sys

# Set Logging level and format
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s: %(levelname)s - %(message)s"
)
# Load .env file
load_dotenv()
# Check imported token is a string
TOKEN = os.getenv("DISCORD_TOKEN")
if isinstance(TOKEN, str) is False:
    logging.error(f"Token given: {TOKEN}")
    raise TypeError("Token is not a string")
else:
    TOKEN = typing.cast(str, TOKEN)
## Intent variables


##Client subclass definition
class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents().all())

    ## On ready event
    async def on_ready(self):
        logging.info(f"{self.user} has connected to Discord!")
        synced = await self.tree.sync()
        logging.info(f"Synced {len(synced)} commands")
        logging.info(f"message content enabled: {self.intents.messages}")

    ## Sync commands
    async def setup_hook(self):
        for folder in os.listdir("cogs"):
            if os.path.exists(os.path.join("cogs", folder, "cog.py")):
                logging.info(f"Loading {folder} cog")
                await self.load_extension(f"cogs.{folder}.cog")


if __name__ == "__main__":
    ## initialise tables
    builder = sessionBuilder()
    builder.initialiseDB()
    ## runs the bot
    client = Client()
    client.run(TOKEN)
    ## closes any remaining open DB sessions if the bot is closed
    close_all_sessions()
