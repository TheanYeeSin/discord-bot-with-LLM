from dotenv import load_dotenv
import os
from typing import Final
from discord import Message, Object
from discord.ext import commands

from DiscordBot.OllamaManager import OllamaManager

load_dotenv()
OLLAMA_URL: Final[str] = os.getenv("OLLAMA_URL")
OLLAMA_MODEL: Final[str] = os.getenv("OLLAMA_MODEL")
SERVER_ID: Final[str] = os.getenv("DISCORD_DEVELOPMENT_SERVER_ID")

ollama_manager = OllamaManager(OLLAMA_URL, OLLAMA_MODEL)


class DiscordBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.assigned_channels = {}

    async def get_message(self, user_message: str) -> str:
        """Send a message to the Ollama model and send the response back to the user"""
        if not user_message:
            print("Message is empty")
            return

        is_private = user_message.startswith("?")
        if is_private:
            user_message = user_message[1:]

        try:
            response: str = ollama_manager.get_response(user_message)
            return response
        except Exception as e:
            print(e)

    # Event handlers
    async def on_ready(self) -> None:
        """Called when the bot is ready"""
        print(f"{self.user} is now running")

        try:
            guild = Object(id=SERVER_ID)
            synced = await self.tree.sync(guild=guild)
            print(f"Synced {len(synced)} commands")
        except Exception as e:
            print(e)

    async def on_message(self, message: Message) -> None:
        """Called when a message is received"""

        if message.author == self.user:
            return

        if message.channel.id not in self.assigned_channels.values():
            return

        username: str = str(message.author)
        user_message: str = message.content
        channel: str = str(message.channel)

        print(f'[{channel}] {username}: "{user_message}"')

        response = await self.get_message(user_message)
        await message.channel.send(response)
