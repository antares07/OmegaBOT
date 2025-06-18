import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import logging
from functions.utils import guild_id

class Timer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot=bot
        self.logger = logging.getLogger("discord")
        self.task = {}

    async def timer(self, duration):
        await asyncio.sleep(duration)

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f'{__name__} loaded')

    @app_commands.command(name='starttimer', description='Start a timer (h:m:s) for an event')
    async def starttimer(self, interaction: discord.Interaction, event: str, hours: int, minutes: int, seconds: int):
        try:
            await interaction.response.send_message(content='Il timer è stato attivato', ephemeral=True)
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming,
                                                                     name='Timer ⏰',
                                                                     state=f'per `{event}` \n della durata di {hours}h:{minutes}m:{seconds}s'), status=discord.Status.online)
            duration = hours * 3600 + minutes * 60 + seconds
            if duration <= 0:
                await interaction.followup.send(content='Durata non valida.', ephemeral=True)
                return
            self.task[interaction.user.id] = asyncio.create_task(self.timer(duration))
            await self.task[interaction.user.id]
            embed = discord.Embed(title=f'{event}', colour=discord.Colour.purple())
            embed.add_field(name=f'Il timer creato da', value=f'{interaction.user.nick}', inline=False)
            embed.add_field(name=f'per', value=f'`{event}`', inline=False)
            embed.add_field(name='e\' terminato!', value='')
            await interaction.channel.send(embed=embed)
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                               name='Giongio\uD83D\uDCA4',
                                                               state='Farmando Focchio'), status=discord.Status.online)
        except Exception as e:
            self.logger.error(f"Error in starttimer command: {e}")
            
    @app_commands.command(name='stoptimer', description='Stop the timer')
    async def stoptimer(self, interaction: discord.Interaction):
        try:
            task = self.task.get(interaction.user.id)
            if task:
                task.cancel()
                del self.task[interaction.user.id]
                await interaction.response.send_message(content=f'Il timer e\' stato disattivato', ephemeral=True)
            else:
                await interaction.response.send_message(content=f'Nessun timer creato da te e\' attivo', ephemeral=True)
        except Exception as e:
            self.logger.error(f"Error in stoptimer command: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Timer(bot), guilds=[guild_id()])