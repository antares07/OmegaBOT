import discord
from discord import app_commands
from discord.ext import commands
import json
import logging
from functions.utils import guild_id

class ChangeNickname(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("config.json") as file:
            self.channel_ids = json.load(file)["channels_id"]
        self.logger = logging.getLogger("discord")

    # Check if command is loaded
    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f'{__name__} loaded')

    # Command for admin
    @app_commands.command(name='nick', description='Change member nickname')
    @app_commands.checks.has_permissions(change_nickname=True)
    async def change_nick(self, interaction: discord.Interaction, member: discord.Member, nickname: str):
        old_nick = member.nick
        await member.edit(nick=nickname)
        await interaction.response.send_message(f'Il nickname di **{old_nick}** e\' stato cambiato da **{old_nick}** in **{nickname}**', ephemeral=True)

    # Automatic change of name when server is joined
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id == self.channel_ids['roles_channel_id'] and message.author.bot:
            return
        elif message.channel.id == self.channel_ids['roles_channel_id']:
            try:
                old_nickname = message.author.display_name
                new_nickname = message.content
                await message.author.edit(nick=new_nickname)
                await message.channel.send(f'Il nickname di {message.author.mention} e\' stato cambiato con successo da **{old_nickname}** a **{new_nickname}**')
            except Exception as e:
                print(e)

async def setup(bot: commands.Bot):
    await bot.add_cog(ChangeNickname(bot), guilds=[guild_id()])