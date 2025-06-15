from discord.ext import commands
from functions.utils import guild_id
import logging

class ReloadCommands(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.logger = logging.getLogger("discord")

    # Check if command is loaded
    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f'{__name__} loaded')

    # Command for admin
    @commands.command(name='reload', description='Sync a given commands')
    async def sync(self, ctx: commands.Context, extension_name: str):
        await self.bot.reload_extension(f'commands.{extension_name}')
        await self.bot.tree.sync(guild=guild_id())
        self.logger.info(f'Reloaded command {extension_name}')
        await ctx.send(f'Reloaded command **{extension_name}**', ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(ReloadCommands(bot), guilds=[guild_id()])