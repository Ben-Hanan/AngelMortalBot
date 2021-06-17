import logging
import player

from config import ANGEL_BOT_TOKEN, PLAYERS_FILENAME

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
players = {}
player.initialize_players(players)

# Helper function for debugging purposes
def printPlayers(players) -> None:
	for player in players:
		player_data = players[player]
		print(f'\t{player_data.username} | {player_data.angel} | {player_data.mortal} | {player_data.chat_id}')

# TODO: Remove this line after done with code, this is for debugging
printPlayers(players)

# Updates .txt file for persistent player profile storage
def updatePlayerProfile(input_user_id, input_username) -> None:
	players_file = open(PLAYERS_FILENAME, "r")	
	players = players_file.readlines()

	for idx, line in enumerate(players):
		data = line.split(",")	
		username = data[0].strip().lower()
		angel = data[1].strip().lower()
		mortal = data[2].strip().lower()

		if username == input_username.lower():
			players[idx] = f'{username}, {angel}, {mortal}, {str(input_user_id)}\n'

	players_file = open(PLAYERS_FILENAME, "w")
	players_file.writelines(players)
	players_file.close()

def start(update: Update, context: CallbackContext) -> None:
	user = update.effective_user
    
	updatePlayerProfile(user.id, user.username)

	update.message.reply_markdown_v2(
		fr'Hi {user.mention_markdown_v2()}\!',
		reply_markup=ForceReply(selective=True),
	)


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')

def forward_message(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

def send_command(update: Update, context: CallbackContext):
    context.bot.send_message(
        text = "Hello World!",
        chat_id = 131189243 
    )

def main() -> None:
    updater = Updater(ANGEL_BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("Send", send_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()