from dotenv import load_dotenv
import os
from typing import Final
from discord import Intents, Client, Message

from DiscordBot.OllamaManager import OllamaManager

OLLAMA_URL: Final[str] = os.getenv("OLLAMA_URL")
OLLAMA_MODEL: Final[str] = os.getenv("OLLAMA_MODEL")


class DiscordBot:
    def __init__(self, token: str) -> None:
        self.token = token

        # Set up the Discord client
        intents: Intents = Intents.default()
        intents.message_content = True
        self.client: Client = Client(intents=intents)

        # Set up the Ollama manager
        self.ollama_manager = OllamaManager(url=OLLAMA_URL, model=OLLAMA_MODEL)

        # Register event handlers
        self.client.event(self.on_ready)
        self.client.event(self.on_message)

    async def send_message(self, message: Message, user_message: str) -> None:
        """Send a message to the Ollama model and send the response back to the user"""
        if not user_message:
            print("Message is empty")
            return

        is_private = user_message.startswith("?")
        if is_private:
            user_message = user_message[1:]

        try:
            response: str = self.ollama_manager.get_response(user_message)
            if is_private:
                await message.author.send(response)
            else:
                await message.channel.send(response)
        except Exception as e:
            print(e)

    async def on_ready(self) -> None:
        """Called when the bot is ready"""
        print(f"{self.client.user} is now running")

    async def on_message(self, message: Message) -> None:
        """Called when a message is received"""
        if message.author == self.client.user:
            return

        username: str = str(message.author)
        user_message: str = message.content
        channel: str = str(message.channel)

        print(f'[{channel}] {username}: "{user_message}"')
        await self.send_message(message, user_message)

    def start(self) -> None:
        """Start the bot"""
        self.client.run(token=self.token)
