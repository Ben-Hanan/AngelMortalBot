import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
PLAYERS_FILENAME = os.environ.get("PLAYERS_FILENAME")
APP_NAME = "angel-mortal-bot"
PORT = int(os.environ.get('PORT', '8443'))
HOST = os.environ.get("HOST")
GOOGLE_SCRIPT = os.environ.get("GOOGLE_SCRIPT")
OPEN_AI = os.environ.get("OPEN_AI")