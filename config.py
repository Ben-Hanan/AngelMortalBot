import os

ANGEL_BOT_TOKEN = os.environ.get("ANGEL_BOT_TOKEN")
MORTAL_BOT_TOKEN = os.environ.get("MORTAL_BOT_TOKEN")
PLAYERS_FILENAME = os.environ.get("PLAYERS_FILENAME")
APP_NAME = "angel-mortal-bot"
PORT = int(os.environ.get('PORT', '8443'))