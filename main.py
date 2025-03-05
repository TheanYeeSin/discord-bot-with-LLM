from DiscordBot import DiscordBot
from dotenv import load_dotenv
import os
from typing import Final
from discord import Intents, Interaction, Object, TextChannel


if __name__ == "__main__":
    # Load env
    load_dotenv()
    DISCORD_TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
    SERVER_ID: Final[str] = os.getenv("DISCORD_DEVELOPMENT_SERVER_ID")

    # Run bot
    intents: Intents = Intents.default()
    intents.message_content = True
    discord_bot = DiscordBot(command_prefix="!", intents=intents)

    GUILD = Object(id=SERVER_ID)

    @discord_bot.tree.command(name="hello", description="Hello command", guild=GUILD)
    async def hello(interaction: Interaction):
        await interaction.response.send_message("Hello!")

    @discord_bot.tree.command(
        name="assign_channel", description="Assign channel command", guild=GUILD
    )
    async def assign_channel(interaction: Interaction, channel: TextChannel):
        discord_bot.assigned_channels[interaction.guild_id] = channel.id
        await interaction.response.send_message("Channel assigned")

    # this command does not work due to limitation of discord api on timeout seconds, try assigning the discord bot to a server channel and talk there
    # @discord_bot.tree.command(
    #     name="prompt", description="Prompt to Ollama command", guild=GUILD
    # )
    # async def prompt(interaction: Interaction, message: str):
    #     response = await discord_bot.get_message(message)
    #     print(response)
    #     await interaction.response.send_message(response)

    discord_bot.run(token=DISCORD_TOKEN)
