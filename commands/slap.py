import discord
from discord import app_commands
from discord.ext import commands
from functions.utils import guild_id
import logging

class Slap(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f'{__name__} loaded')

    @app_commands.command(name='slap', description='Slap a member of the server')
    @app_commands.guilds(guild_id())
    async def slap(self, interaction:discord.Interaction, member: discord.Member, reason: str):
        user = interaction.user.mention
        slapped = member.mention
        await interaction.response.send_message(content=f'{user} ha colpito {slapped} per: **{reason}**')

async def setup(bot: commands.Bot):
    await bot.add_cog(Slap(bot), guilds=[guild_id()])