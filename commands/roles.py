import discord
from discord.ext import commands
from discord import app_commands
import logging
import json
from functions.utils import guild_id

#Class for role buttons
class Buttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        with open("config.json") as file:
            self.role_ids = json.load(file)["roles"]
    
    @discord.ui.button(label='Warframe', style=discord.ButtonStyle.blurple, custom_id='warframe_role_button')
    async def warframe(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Defer the response to avoid "interaction failed" if there's a slight delay.
        await interaction.response.defer(ephemeral=True)

        # Get the role from the guild using the ID.
        role_id = self.role_ids['warframe']
        warframe_role = interaction.guild.get_role(role_id)

        if warframe_role is None:
            # This can happen if the role was deleted.
            await interaction.followup.send("Error: The 'Warframe' role could not be found on this server. Please contact an admin.")
            return

        # --- THIS IS THE CORRECTED LOGIC ---
        # Check if the discord.Role object is directly in the user's list of roles.
        if warframe_role in interaction.user.roles:
            # User has the role, so we remove it.
            try:
                await interaction.user.remove_roles(warframe_role)
                # Send a confirmation message that only the user can see.
                await interaction.followup.send(f"Il ruolo **{warframe_role.name}** è stato rimosso.", ephemeral=True)
            except discord.Forbidden:
                await interaction.followup.send("I don't have permission to remove your roles. Please check my permissions and role hierarchy.", ephemeral=True)
            except Exception as e:
                print(e)
                await interaction.followup.send("An unexpected error occurred while trying to remove the role.", ephemeral=True)
        else:
            # User does not have the role, so we add it.
            try:
                await interaction.user.add_roles(warframe_role)
                # Send a confirmation message that only the user can see.
                await interaction.followup.send(f"Ora hai il ruolo **{warframe_role.name}**!", ephemeral=True)
            except discord.Forbidden:
                await interaction.followup.send("I don't have permission to give you this role. Please check my permissions and role hierarchy.", ephemeral=True)
            except Exception as e:
                print(e)
                await interaction.followup.send("An unexpected error occurred while trying to add the role.", ephemeral=True)

    @discord.ui.button(label='R6', style=discord.ButtonStyle.red, custom_id='r6_role_button')
    async def r6(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Defer the response to avoid "interaction failed" if there's a slight delay.
        await interaction.response.defer(ephemeral=True)

        # Get the role from the guild using the ID.
        role_id = self.role_ids['r6']
        r6_role = interaction.guild.get_role(role_id)

        if r6_role is None:
            # This can happen if the role was deleted.
            await interaction.followup.send("Error: The 'R6' role could not be found on this server. Please contact an admin.")
            return

        # --- THIS IS THE CORRECTED LOGIC ---
        # Check if the discord.Role object is directly in the user's list of roles.
        if r6_role in interaction.user.roles:
            # User has the role, so we remove it.
            try:
                await interaction.user.remove_roles(r6_role)
                # Send a confirmation message that only the user can see.
                await interaction.followup.send(f"Il ruolo **{r6_role.name}** è stato rimosso.", ephemeral=True)
            except discord.Forbidden:
                await interaction.followup.send("I don't have permission to remove your roles. Please check my permissions and role hierarchy.", ephemeral=True)
            except Exception as e:
                print(e)
                await interaction.followup.send("An unexpected error occurred while trying to remove the role.", ephemeral=True)
        else:
            # User does not have the role, so we add it.
            try:
                await interaction.user.add_roles(r6_role)
                # Send a confirmation message that only the user can see.
                await interaction.followup.send(f"Ora hai il ruolo **{r6_role.name}**!", ephemeral=True)
            except discord.Forbidden:
                await interaction.followup.send("I don't have permission to give you this role. Please check my permissions and role hierarchy.", ephemeral=True)
            except Exception as e:
                print(e)
                await interaction.followup.send("An unexpected error occurred while trying to add the role.", ephemeral=True)

    @discord.ui.button(label='LOL', style=discord.ButtonStyle.green, custom_id='lol_role_button')
    async def lol(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Defer the response to avoid "interaction failed" if there's a slight delay.
        await interaction.response.defer(ephemeral=True)

        # Get the role from the guild using the ID.
        role_id = self.role_ids['lol']
        lol_role = interaction.guild.get_role(role_id)

        if lol_role is None:
            # This can happen if the role was deleted.
            await interaction.followup.send("Error: The 'lol' role could not be found on this server. Please contact an admin.")
            return

        # --- THIS IS THE CORRECTED LOGIC ---
        # Check if the discord.Role object is directly in the user's list of roles.
        if lol_role in interaction.user.roles:
            # User has the role, so we remove it.
            try:
                await interaction.user.remove_roles(lol_role)
                # Send a confirmation message that only the user can see.
                await interaction.followup.send(f"Il ruolo **{lol_role.name}** è stato rimosso.", ephemeral=True)
            except discord.Forbidden:
                await interaction.followup.send("I don't have permission to remove your roles. Please check my permissions and role hierarchy.", ephemeral=True)
            except Exception as e:
                print(e)
                await interaction.followup.send("An unexpected error occurred while trying to remove the role.", ephemeral=True)
        else:
            # User does not have the role, so we add it.
            try:
                await interaction.user.add_roles(lol_role)
                # Send a confirmation message that only the user can see.
                await interaction.followup.send(f"Ora hai il ruolo **{lol_role.name}**!", ephemeral=True)
            except discord.Forbidden:
                await interaction.followup.send("I don't have permission to give you this role. Please check my permissions and role hierarchy.", ephemeral=True)
            except Exception as e:
                print(e)
                await interaction.followup.send("An unexpected error occurred while trying to add the role.", ephemeral=True)

class RolesButton(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        with open("config.json") as file:
            self.channel_ids = json.load(file)["channels_id"]
        # The super().__init__() is important for cogs using persistent views
        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f'{__name__} loaded')
        # Since Buttons is a persistent view (timeout=None), we register it on startup.
        # This ensures the buttons work even after the bot restarts.
        self.bot.add_view(Buttons())

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        try:
            nick_channel: discord.TextChannel = self.channel_ids['roles_channel_id']
            guild_name = member.guild.name
            embed = discord.Embed(
                title=f'Salve Tenno! Sono {self.bot.user.name}, il **protettore** di {guild_name}',
                colour=discord.Colour.purple()
            )
            embed.add_field(name='Cosa devi fare ora:', value='Selezionare uno o più ruoli cliccando i pulsanti qui sotto.', inline=False)
            embed.add_field(name='Successivamente:', value='Scrivi il tuo nickname in-game sulla chat di questo canale e io magicamente cambierò il nickname su questo server', inline=False)

            await nick_channel.send(embed=embed, view=Buttons())
        
        except Exception as e:
            self.logger.error(f"Error in /roles command: {e}")

    @app_commands.command(name='roles', description='Sends the role selection menu.')
    @app_commands.guilds(guild_id()) # Restrict to your guild for instant updates
    async def rolebuttons(self, interaction: discord.Interaction):
        #Sends the role selection embed with buttons.
        try:
            guild_name = interaction.guild.name
            embed = discord.Embed(
                title=f'Salve Tenno! Sono {self.bot.user.name}, il **protettore** di {guild_name}',
                colour=discord.Colour.purple()
            )
            embed.add_field(name='Cosa devi fare ora:', value='Selezionare uno o più ruoli cliccando i pulsanti qui sotto.', inline=False)
            embed.add_field(name='Successivamente:', value='Scrivi il tuo nickname in-game sulla chat di questo canale e io magicamente cambierò il nickname su questo server', inline=False)

            # Send the message with the embed and the persistent view
            await interaction.response.send_message(embed=embed, view=Buttons())
        except Exception as e:
            self.logger.error(f"Error in /roles command: {e}")
            if not interaction.response.is_done():
                await interaction.response.send_message("An error occurred while executing the command.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(RolesButton(bot), guilds=[guild_id()])
