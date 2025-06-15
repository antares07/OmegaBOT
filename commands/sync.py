from discord.ext import commands
from functions.utils import guild_id
import logging

class SyncCommands(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.logger = logging.getLogger("discord")

    # Check if command is loaded
    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f'{__name__} loaded')

    # Command for admin
    @commands.command(name='sync', description='Sync all commands')
    async def sync(self, ctx: commands.Context):
        cogs = await self.bot.tree.sync(guild=guild_id())
        self.logger.info(f'Syncronized {len(cogs)} command(s): {[cog.name for cog in cogs]}')
        await ctx.send(f'Syncronized {len(cogs)} command(s)', ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(SyncCommands(bot))
