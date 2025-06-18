import discord
from discord import app_commands
from discord.ext import commands
import logging
import aiosqlite
import os
from functions.utils import guild_id
from typing import Optional
from collections import Counter

DB_FILE = 'currency.db'

class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.db_path = DB_FILE

    async def init_db(self):
        async with aiosqlite.connect(self.db_path) as db:
            # Create the users table if it doesn't exist
            # user_id: TEXT PRIMARY KEY (Discord user ID)
            # balance: INTEGER (or REAL for decimal currency if needed)
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    balance INTEGER DEFAULT 0
                )
            ''')
            await db.commit() # Commit the changes to save the table

    async def get_balance(self, user_id: str) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
            result = await cursor.fetchone()
            if result:
                return result[0] # Return the balance
            else:
                # If user not found, create them with a default balance of 0
                await db.execute('INSERT INTO users (user_id, balance) VALUES (?, ?)', (user_id, 0))
                await db.commit()
                return 0
            
    async def update_balance(self, user_id: str, amount: int):
        async with aiosqlite.connect(self.db_path) as db:
            # Check if the user exists
            cursor = await db.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
            user_exists = await cursor.fetchone()

            if user_exists:
                # Update existing user's balance
                await db.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
            else:
                # Insert new user with the given amount (e.g., for initial daily reward)
                await db.execute('INSERT INTO users (user_id, balance) VALUES (?, ?)', (user_id, amount))
            await db.commit()

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f'{__name__} loaded')
        await self.init_db()
        self.logger.info(f'Database initialized')

    @app_commands.command(name='currency', description='Controlla il tuo saldo')
    async def check_currency(self, interaction: discord.Interaction, member: Optional[discord.Member]):
        try:
            target_member = member or interaction.user
            user_id = str(target_member.id)

            balance = await self.get_balance(user_id)

            if member:
                embed = discord.Embed(title=f'Salve Tenno! Ecco il conto di {member.nick}', colour=discord.Colour.purple())
                embed.add_field(name='Totale', value=f'{member.nick} ha in totale {balance} **giongi**', inline=False)
                if balance<=100:
                    embed.add_field(name='Che poveraccio', value='💩')
            else:
                embed = discord.Embed(title=f'Salve Tenno! Ecco il tuo conto', colour=discord.Colour.purple())
                embed.add_field(name='Totale', value=f'Hai in totale {balance} **giongi**', inline=False)
                if balance<=100:
                    embed.add_field(name='Che poveraccio che sei', value='💩')

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            self.logger.error(f"Error in currency command: {e}")
            await interaction.response.send_message("Si è verificato un errore nel recuperare il saldo.", ephemeral=True)

    @app_commands.command(name='addcurrency', description='Aggiungi giongi a un utente (admin only)')
    @app_commands.checks.has_permissions(administrator=True)
    async def add_currency(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        try:
            if amount <= 0:
                await interaction.response.send_message("L'importo deve essere maggiore di zero.", ephemeral=True)
                return

            user_id = str(member.id)
            await self.update_balance(user_id, amount)
            new_balance = await self.get_balance(user_id) # Get the updated balance

            await interaction.response.send_message(f"Hai aggiunto {amount} **giongi** a {member.mention}. Ora ha {new_balance} **giongi**.")

        except Exception as e:
            self.logger.error(f"Error in addcurrency command: {e}")
            await interaction.response.send_message("Errore durante l'aggiunta di giongi.", ephemeral=True)

    @app_commands.command(name='removecurrency', description='Rimuovi giongi a un utente (admin only).')
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_currency(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        try:
            if amount <= 0:
                await interaction.response.send_message("L'importo deve essere maggiore di zero.", ephemeral=True)
                return

            user_id = str(member.id)
            # Subtract the amount (pass a negative value to update_balance)
            await self.update_balance(user_id, -amount)
            new_balance = await self.get_balance(user_id)

            await interaction.response.send_message(f"Hai rimosso {amount} **giongi** a {member.mention}. Ora ha {new_balance} **giongi**.")

        except Exception as e:
            self.logger.error(f"Error in removecurrency command: {e}")
            await interaction.response.send_message("Errore durante la rimozione di giongi.", ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        try:

            # Ignore messages from the bot itself
            if message.author == self.bot.user:
                return
            
            # Ignore messages from bots to prevent unintended currency gains/losses
            if message.author.bot:
                return
        
            user_id = str(message.author.id)
            
            # Process message content
            words_list = list(message.content.lower().split())
            word_list_len = len(words_list)
            words_counter = Counter(words_list)

            # Check for specific "magic" or "cursed" words
            giongio_count = words_counter.get('giongio', 0)
            giongiofocchio_count = words_counter.get('giongiofocchio', 0)

            if giongio_count > 0:
                amount_to_add = giongio_count * 10000 + word_list_len * 100
                await self.update_balance(user_id, amount_to_add)
                await message.channel.send(
                    f'Hai trovato la parola magica {message.author.mention}! '
                    f'Ti sono stati aggiunti {amount_to_add} **giongi**.'
                )
            elif giongiofocchio_count > 0:
                amount_to_remove = giongiofocchio_count * 10000 + word_list_len * 100
                # Pass a negative value to subtract currency
                await self.update_balance(user_id, -amount_to_remove) 
                await message.channel.send(
                    f'Hai trovato la parola maledetta {message.author.mention}! '
                    f'Ti sono stati tolti {amount_to_remove} **giongi**.'
                )
            else:
                # Award currency based on total words if no special words are found
                amount_to_add = len(words_list) * 100 # Count words in the list directly
                await self.update_balance(user_id, amount_to_add)

        except Exception as e:
            self.logger.error(f"Error in checking message for currency: {e}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Currency(bot), guilds=[guild_id()])
