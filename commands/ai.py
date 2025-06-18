import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import json
import logging
from typing import Optional
from functions.utils import guild_id

# --- Configuration for Ollama ---
# Replace with your Ollama server URL if it's not local
OLLAMA_API_BASE_URL = "http://localhost:11434"
# The name of the Ollama model you want to use (e.g., 'llama3', 'mistral', 'gemma')
DEFAULT_OLLAMA_MODEL = "llama3.2" 
# Max characters for a Discord message (2000)
DISCORD_MESSAGE_CHAR_LIMIT = 1900 # Leave some room for "..."

class OllamaAI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.session = aiohttp.ClientSession() # Create an aiohttp session for HTTP requests

    async def cog_unload(self):
        """Close the aiohttp session when the cog is unloaded."""
        await self.session.close()
        self.logger.info(f'{__name__} aiohttp session closed.')

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f'{__name__} loaded.')

    async def send_to_ollama(self, prompt: str, model_name: str = DEFAULT_OLLAMA_MODEL):
        """
        Sends a prompt to the Ollama API and returns the generated response.
        Returns None if an error occurs.
        """
        url = f"{OLLAMA_API_BASE_URL}/api/generate"
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False # We want a single, complete response
        }

        try:
            async with self.session.post(url, json=payload, timeout=500) as response: # 5 minute timeout for long generations
                response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
                
                response_data = await response.json()
                
                # The actual response text is in the 'response' key
                if 'response' in response_data:
                    return response_data['response'].strip()
                else:
                    self.logger.warning(f"Ollama API response missing 'response' key: {response_data}")
                    return None
        except aiohttp.ClientConnectorError as e:
            self.logger.error(f"Failed to connect to Ollama server at {OLLAMA_API_BASE_URL}: {e}")
            return None
        except aiohttp.ClientResponseError as e:
            self.logger.error(f"Ollama API returned an error status {e.status}: {e.message}")
            if e.status == 404: # Model not found
                return f"Errore: Il modello Ollama '{model_name}' non è stato trovato. Assicurati che sia installato (es. `ollama pull {model_name}`)."
            return None
        except aiohttp.ClientError as e:
            self.logger.error(f"Error communicating with Ollama API: {e}")
            return None
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON response from Ollama API.")
            return None
        except Exception as e:
            self.logger.error(f"An unexpected error occurred in send_to_ollama: {e}")
            return None

    @app_commands.command(name='ask_ai', description='Fai una domanda al modello AI locale (Ollama).')
    @app_commands.describe(
        question='La tua domanda per l\'AI.',
        model='(Opzionale) Il nome del modello Ollama da usare (es. llama3, mistral). Predefinito: ' + DEFAULT_OLLAMA_MODEL
    )
    async def ask_ai_command(self, interaction: discord.Interaction, question: str, model: Optional[str] = None):
        """Sends a question to the configured Ollama AI model."""
        await interaction.response.defer(thinking=True) # Show "Bot is thinking..."

        chosen_model = model if model else DEFAULT_OLLAMA_MODEL
        
        # Add a basic prompt structure, you can make this more complex
        full_prompt = f"{question}" 

        self.logger.info(f"User {interaction.user.name} asked AI ({chosen_model}): {question}")
        
        answer = await self.send_to_ollama(full_prompt, chosen_model)

        if answer:
            # Truncate if the answer is too long for Discord
            if len(answer) > DISCORD_MESSAGE_CHAR_LIMIT:
                answer = answer[:DISCORD_MESSAGE_CHAR_LIMIT] + "..." # Truncate with ellipsis
                await interaction.followup.send(
                    f"**Risposta di {chosen_model} (troncata):**\n"
                    f"{answer}",
                    ephemeral=False # Visible to everyone
                )
            else:
                await interaction.followup.send(
                    f"**Risposta di {chosen_model}:**\n"
                    f"{answer}",
                    ephemeral=False
                )
        else:
            await interaction.followup.send(
                "Mi dispiace, non sono riuscito a ottenere una risposta dall'AI. "
                "Controlla che il server Ollama sia in esecuzione e che il modello "
                f"`{chosen_model}` sia installato (`ollama run {chosen_model}`). "
                "Controlla anche i log del bot per maggiori dettagli sull'errore.",
                ephemeral=True # Only visible to the user who ran the command
            )

async def setup(bot: commands.Bot):
    await bot.add_cog(OllamaAI(bot), guilds=[guild_id()])