import discord
from discord.ext import commands
from collections import Counter
import logging

class MosDetection(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.logger = logging.getLogger("discord")
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f'{__name__} loaded')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        
        words_list = list(message.content.lower().split())
        words_counter = Counter(words_list)
        
        if message.author == self.bot.user:
            return
        
        if words_counter['mos'] > 0:
            await message.channel.send(f'Basta rotolare {message.author.mention}')

async def setup(bot: commands.Bot):
    await bot.add_cog(MosDetection(bot))