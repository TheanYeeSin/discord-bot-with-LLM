import requests


class OllamaManager:

    def __init__(self, url: str, model: str) -> None:
        # Set up the Ollama manager
        self.url = url
        self._message_history = []
        self._messages = {
            "model": model,
            "messages": self._message_history,
            "stream": False,
        }

    def get_response(self, user_input: str) -> str:
        """Get a response from the Ollama model"""
        self._message_history.append({"role": "user", "content": user_input})

        try:
            response = requests.post(f"{self.url}/api/chat", json=self._messages)
            data = response.json()
            bot_message: str = data["message"]["content"]
            self._message_history.append({"role": "assistant", "content": bot_message})
            return bot_message

        except Exception as e:
            print(e)
