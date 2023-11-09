import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import logging
import typing


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

    async def on_ready(self):
        logging.info(f"{self.user} has connected to Discord!")
        synced = await self.tree.sync()
        logging.info(f"Synced {len(synced)} commands")
        logging.info(f"message content enabled: {self.intents.messages}")

    async def setup_hook(self):
        for folder in os.listdir("cogs"):
            if os.path.exists(os.path.join("cogs", folder, "cog.py")):
                logging.info(f"Loading {folder} cog")
                await self.load_extension(f"cogs.{folder}.cog")


client = Client()
client.run(TOKEN)
