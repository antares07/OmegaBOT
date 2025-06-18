import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import logging
from typing import Optional
from functions.utils import guild_id

# Base URL for the Warframe Worldstate API
WARFRAME_WORLDSTATE_API_URL = "https://api.warframestat.us/pc" # Targeting PC platform

class WarframeInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.session = aiohttp.ClientSession() # Create an aiohttp session for HTTP requests

    async def cog_unload(self):
        # Close the aiohttp session when the cog is unloaded
        await self.session.close()
        self.logger.info(f'{__name__} session closed.')

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f'{__name__} loaded.')

async def setup(bot: commands.Bot):
    await bot.add_cog(WarframeInfo(bot), guilds=[guild_id()])