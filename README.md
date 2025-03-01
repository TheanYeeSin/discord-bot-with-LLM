# Discord-bot

Discord-bot made in Python

## Installation

1. Clone the repo

```
git clone
```

2. Start a virtual environment [Optional]

```
python -m venv venv
```

3. Activate your virtual environment [Optional]

Note: In Powershell
```
venv\Scripts\Activate
```

4. Install packages

```
pip install -r requirements.txt
```

5. Setup .env file (refers to `.env.example`)

```
vim .env
```

6. Setup Ollama

```
docker-compose -f docker-compose-ollama.yml up
```

7. Start the bot

```
python main.py
```

