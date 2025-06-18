import discord
from discord.ext import commands
from collections import Counter
import logging
from functions.utils import guild_id

class MosDetection(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.logger = logging.getLogger("discord")
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f'{__name__} loaded')

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        try:
            words_list = list(message.content.lower().split())
            words_counter = Counter(words_list)
            
            if words_counter['mos'] > 0 and message.author != self.bot.user:
                await message.channel.send(f'Basta rotolare {message.author.mention}')
            #elif words_counter['giongio'] > 0 or words_counter['<@723962095095382047>'] > 0 or words_counter['giongiofocchio']:
            #    await message.channel.send(f'Anche tu vuoi giocare a Roblox {message.author.mention}? E invece ti banno')

        except Exception as e:
            self.logger.error(f"Error in currency command: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(MosDetection(bot), guilds=[guild_id()])