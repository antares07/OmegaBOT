import discord
from discord import app_commands
from discord.ext import commands
import logging
from functions.utils import guild_id

class AlertMessage(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f'{__name__} loaded')

    @app_commands.command(name='alert', description='Send an alert message with the bot')
    @app_commands.guilds(guild_id())
    async def alert_message(self, interaction: discord.Interaction, message: str):
        try:
            embed = discord.Embed(title=f'Salve Tenno! Il grande capo {self.bot.get_guild(guild_id(False)).owner.nick} richiede la vostra attenzione',
                                  colour=discord.Colour.purple())
            embed.add_field(name=f':bangbang:`{message}`:bangbang:', value='', inline=False)
            embed.add_field(name='Grazie a tutti per l\'attenzione', value='Potete tornare ai vostri sporchi affari...')
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            self.logger.error(f"Error in alert message: {e}")
            
async def setup(bot: commands.Bot):
    await bot.add_cog(AlertMessage(bot), guilds=[guild_id()])