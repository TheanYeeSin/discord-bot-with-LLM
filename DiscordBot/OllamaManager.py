import requests
from DiscordBot.Logger import logger


class OllamaManager:

    def __init__(self, url: str, model: str) -> None:
        # Set up the Ollama manager
        logger.debug("[OllamaManager] Setting up Ollama manager")
        self.url = url
        self._message_history = []
        self._messages = {
            "model": model,
            "messages": self._message_history,
            "stream": False,
        }

    def get_response(self, user_input: str) -> str:
        """Get a response from the Ollama model"""
        logger.info(
            f"[OllamaManager] Getting response from Ollama model for {user_input}"
        )
        self._message_history.append({"role": "user", "content": user_input})

        try:
            response = requests.post(f"{self.url}/api/chat", json=self._messages)
            data = response.json()
            bot_message: str = data["message"]["content"]
            self._message_history.append({"role": "assistant", "content": bot_message})
            logger.info("[OllamaManager] Successfully got response from Ollama model")
            return bot_message

        except Exception as e:
            logger.error(
                f"[OllamaManager] Error getting response from Ollama model: {e}"
            )
