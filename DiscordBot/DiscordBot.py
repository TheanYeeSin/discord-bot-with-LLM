from dotenv import load_dotenv
import os
from typing import Final
from discord import Message, Object
from discord.ext import commands
from DiscordBot.Logger import logger

from DiscordBot.OllamaManager import OllamaManager

load_dotenv()
OLLAMA_URL: Final[str] = os.getenv("OLLAMA_URL")
OLLAMA_MODEL: Final[str] = os.getenv("OLLAMA_MODEL")
SERVER_ID: Final[str] = os.getenv("DISCORD_DEVELOPMENT_SERVER_ID")

ollama_manager = OllamaManager(OLLAMA_URL, OLLAMA_MODEL)


class DiscordBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        logger.debug("[DiscordBot] Setting up Discord bot")
        super().__init__(*args, **kwargs)
        self.assigned_channels = {}

    async def get_message(self, user_message: str) -> str:
        """Send a message to the Ollama model and send the response back to the user"""
        logger.info(
            f"[DiscordBot] Getting response from Ollama Manager for {user_message}"
        )
        if not user_message:
            logger.info("User message is empty")
            return

        try:
            response: str = ollama_manager.get_response(user_message)
            logger.info("[DiscordBot] Successfully got response from Ollama Manager")
            return response
        except Exception as e:
            logger.error(
                f"[DiscordBot] Error getting response from Ollama Manager: {e}"
            )

    # Event handlers
    async def on_ready(self) -> None:
        """Called when the bot is ready"""
        logger.info(f"[DiscordBot] {self.user} is now running")

        try:
            guild = Object(id=SERVER_ID)
            synced = await self.tree.sync(guild=guild)
            logger.info(f"[DiscordBot] Synced commands: {len(synced)} commands")
        except Exception as e:
            logger.error(f"[DiscordBot] Error syncing commands: {e}")

    async def on_message(self, message: Message) -> None:
        """Called when a message is received"""

        logger.debug(f"[DiscordBot] Received message from {message.author}")

        if message.author == self.user:
            logger.debug("[DiscordBot] Message from bot")
            return

        if message.channel.id not in self.assigned_channels.values():
            logger.debug("[DiscordBot] Message from unassigned channel")
            return

        username: str = str(message.author)
        user_message: str = message.content
        channel: str = str(message.channel)

        logger.info(
            f"[DiscordBot] Received message from {username} in {channel} with content {user_message}"
        )

        response = await self.get_message(user_message)
        await message.channel.send(response)
