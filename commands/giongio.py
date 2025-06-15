import discord
from discord import app_commands
from discord.ext import commands
import logging
from functions.utils import guild_id

class Giongio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f'{__name__} loaded')

    @app_commands.command(name='giongio', description='Answer focchio')
    @app_commands.guilds(guild_id())
    async def answer_giongio(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_message(f'Focchio')
        except Exception as e:
            print(e)

async def setup(bot: commands.Bot):
    await bot.add_cog(Giongio(bot), guilds=[guild_id()])