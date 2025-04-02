import discord
from discord.ext import commands
import json
from functions.utils import get_config_path
import logging

class ChangeNickname(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open(get_config_path("config.json")) as file:
            self.channel_ids = json.load(file)["channels_id"]
        self.logger = logging.getLogger("discord")

    # Check if command is loaded
    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f'{__name__} loaded')

    # Command for admin
    @commands.command(name='nick', description='Change member nickname')
    @commands.has_permissions(change_nickname=True)
    async def change_nick(self, interaction: discord.Interaction, member: discord.Member, nickname: str):
        await member.edit(nick=nickname)
        await interaction.response.send_message(f'Il nickname e\' stato aggiornato con successo', ephemeral=True)

    # Automatic change of name when server is joined
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.channel_ids['only_sup_id'] and message.author.bot:
            return
        elif message.channel.id == self.channel_ids['only_sup_id']:
            try:
                old_nickname = message.author.display_name
                new_nickname = message.content
                await message.author.edit(nick=new_nickname)
                await message.channel.send(f'Il nickname di {message.author.mention} cambiato con successo da **{old_nickname}** a **{new_nickname}**')
            except Exception as e:
                print(e)

async def setup(bot):
    await bot.add_cog(ChangeNickname(bot))