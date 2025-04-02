import discord
from discord.ext import commands
import os
from config import token

class MyBot(commands.Bot):
    def __init__(self, command_prefix, intents):
        super().__init__(command_prefix=command_prefix, intents=intents)

    async def load_all_cogs(self):
        # Dynamically load all cogs from the 'cogs' directory
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                print(f"Loaded cog: {filename[:-3]}")

    async def on_ready(self):
        print(f'Logged in as {self.user.name}')

def main():
    intents = discord.Intents.all()
    bot = MyBot(command_prefix="!", intents=intents)
    bot.load_all_cogs()
    bot.run(token())
