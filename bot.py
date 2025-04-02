import discord
from discord.ext import commands
import os
from functions.config import token
import logging

class MyBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.logger = logging.getLogger("discord")

    async def setup_hook(self):
        # Dynamically load all cogs from the 'cogs' directory
        for filename in os.listdir('./commands'):
            if filename.endswith('.py'):
                await self.load_extension(f'commands.{filename[:-3]}')

    async def on_ready(self):
        # Change status of the bot
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                             name='Giongio\uD83D\uDCA4',
                                                             state='Farmando Focchio'), status=discord.Status.online)
        self.logger.info(f'Logged in as {self.user.name}')

def main():
    intents = discord.Intents.all()
    bot = MyBot(command_prefix="!", intents=intents)
    bot.run(token())
