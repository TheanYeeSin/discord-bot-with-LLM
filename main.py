from DiscordBot import DiscordBot
from dotenv import load_dotenv
import os
from typing import Final


if __name__ == "__main__":
    load_dotenv()
    DISCORD_TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
    discord_bot = DiscordBot(token=DISCORD_TOKEN)
    discord_bot.start()
