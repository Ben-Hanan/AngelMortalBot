import logging
import messages
import player
from collections import defaultdict

from config import BOT_TOKEN, HOST, PORT, APP_NAME, HEROKU_LINK
from utils import updateGoogleSheetsPlayers, promptAi, UPDATE_SUCCESSFUL, UPDATE_UNSUCCESSFUL

from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

# Enable logging
logging.basicConfig(
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
players = defaultdict(player.Player)
player.initialize_players(players)

parse_mode = 'MarkdownV2'

# Helper function for debugging purposes
def printPlayers(players) -> None:
	for player in players:
		player_data = players[player]
		print(f'\t{player_data.username} | {player_data.angel} | {player_data.mortal} | {player_data.chat_id}')

def start(update: Update, context: CallbackContext) -> None:
	user = update.effective_user
	username = user.username.lower()

	response = updateGoogleSheetsPlayers(user.username, user.id)
	response_code = response['result'][-3:]

	logger.info(f'updated google sheet for {username} and input chat_id {players[username].chat_id}')

	player.initialize_players(players)
	players[username].chat_id = user.id

	logger.info(f'{username} started the bot with chat_id {players[username].chat_id}')

	if response_code == UPDATE_SUCCESSFUL:
		player.initialize_players(players)
		players[user.username.lower()].chat_id = user.id
		update.message.reply_markdown_v2(
			fr'Hi {user.mention_markdown_v2()}\!'
			+ messages.format_start_message()
		)
	elif response_code == UPDATE_UNSUCCESSFUL:
		update.message.reply_markdown_v2(
			fr'Hi {user.mention_markdown_v2()}\!'
			+ messages.NOT_INITIALIZED
	)

def reveal_mortal_command(update: Update, context: CallbackContext) -> None:
	user = update.effective_user
	mortal = players[user.username.lower()].mortal

	if mortal is None:
		update.message.reply_text(messages.MORTAL_NOT_FOUND)
		logger.error(f'could not find mortal for {players[user.username.lower()]}')
	else:
		keyboard = [
			[
				InlineKeyboardButton("Reveal!", callback_data='reveal'),
			],
		]

		reply_markup = InlineKeyboardMarkup(keyboard)

		update.message.reply_text('Your mortal is...', reply_markup=reply_markup)        

def reveal_mortal(update: Update, context: CallbackContext):
    user = update.effective_user
    mortal = players[user.username.lower()].mortal

    context.bot.answerCallbackQuery(
        callback_query_id=update.callback_query.id, 
    )

    update.callback_query.message.edit_text(text=messages.format_mortal_reveal(mortal))

#TODO: Update help command
def help_command(update: Update, context: CallbackContext) -> None:
	update.message.reply_text(messages.format_help_message())

def generate_text(update: Update, context: CallbackContext) -> None:
	prompt = update.message.text
	message = promptAi(prompt)
	context.bot.send_message(message.chat.id, message)

def forward_message(update: Update, context: CallbackContext) -> None:
	"""Send a message to either the Angel or Mortal depending on the mode set"""
	user = update.effective_user
	curr_user = user.username.lower()

	if players[curr_user].is_recipient_angel is None:
		update.message.reply_text(messages.CHOOSE_RECIPIENT)
		logger.warning(f'{curr_user} has not chosen the recipient for their messages')
	else:
		try:
			if players[curr_user].is_recipient_angel is True:
				angel_chat_id = players[curr_user].angel.chat_id
				if angel_chat_id is None:
					update.message.reply_text(messages.BOT_NOT_STARTED)
					logger.warning(f'{curr_user} tried to contact their angel but their angel has not started this bot')
					return
				else:
					context.bot.send_message(
						text=messages.format_mortal_message(update.message.text),
						chat_id=angel_chat_id,
					)
			
			if players[curr_user].is_recipient_angel is False:
				mortal_chat_id = players[curr_user].mortal.chat_id
				if mortal_chat_id is None:
					update.message.reply_text(messages.BOT_NOT_STARTED)
					logger.warning(f'{curr_user} tried to contact their mortal but their mortal has not started this bot')
					return
				else:
					context.bot.send_message(
						text=messages.format_angel_message(update.message.text),
						chat_id=mortal_chat_id,
					)
		except Exception as e:
			logger.error(f'{curr_user} failed to send a message')
			update.message.reply_text(messages.MESSAGE_SEND_FAIL)
			

def set_recipient_angel(update: Update, context: CallbackContext) -> None:
	user = update.effective_user
	curr_user = user.username.lower()

	if (players[curr_user].is_recipient_angel is True):
		update.callback_query.message.edit_text(messages.ALREADY_TEXTING_ANGEL)
	else:
		players[curr_user].is_recipient_angel = True
		context.bot.answerCallbackQuery(
			callback_query_id=update.callback_query.id, 
			text=messages.CHATTING_WITH_ANGEL,
			show_alert=True
		)
		pin_message_id = update.callback_query.message.edit_text(
							text=messages.CHATTING_WITH_ANGEL
						).message_id
		context.bot.unpinAllChatMessages(user.id)
		context.bot.pinChatMessage(user.id, pin_message_id)

def set_recipient_mortal(update: Update, context: CallbackContext) -> None:
	user = update.effective_user
	curr_user = user.username.lower()

	if (players[curr_user].is_recipient_angel is False):
		update.callback_query.message.edit_text(text=messages.ALREADY_TEXTING_MORTAL)
	else:
		players[curr_user].is_recipient_angel = False
		context.bot.answerCallbackQuery(
			callback_query_id=update.callback_query.id, 
			text=messages.CHATTING_WITH_MORTAL,
			show_alert=True
		)
		pin_message_id = update.callback_query.message.edit_text(
							text=messages.CHATTING_WITH_MORTAL
						).message_id
		context.bot.unpinAllChatMessages(user.id)
		context.bot.pinChatMessage(user.id, pin_message_id)


def set_message_recipient(update: Update, context: CallbackContext) -> None:
	keyboard = [
		[
			InlineKeyboardButton("Angel", callback_data='angel'),
			InlineKeyboardButton("Mortal", callback_data='mortal'),
		],
	]

	reply_markup = InlineKeyboardMarkup(keyboard)

	update.message.reply_text('Choose who to chat with!', reply_markup=reply_markup)

def forward_photo_message(update: Update, context: CallbackContext) -> None:
	user = update.effective_user
	curr_user = user.username.lower()

	image_id = update.message.photo[len(update.message.photo)-1].file_id
	"""
	file_path = context.bot.get_file(image_id).file_path
	image_url = "https://api.telegram.org/file/bot{0}/{1}".format(BOT_TOKEN, file_path)
	"""

	if players[curr_user].is_recipient_angel is None:
		update.message.reply_text(messages.CHOOSE_RECIPIENT)
		logger.warning(f'{curr_user} has not chosen the recipient for their photo messages')
	else:
		try:
			if players[curr_user].is_recipient_angel is True:
				angel_chat_id = players[curr_user].angel.chat_id
				if angel_chat_id is None:
					update.message.reply_text(messages.BOT_NOT_STARTED)
					logger.warning(f'{curr_user} tried to contact their angel but their angel has not started this bot')
					return
				else:
					context.bot.send_photo(chat_id=angel_chat_id, photo=image_id)
			
			if players[curr_user].is_recipient_angel is False:
				mortal_chat_id = players[curr_user].mortal.chat_id
				if mortal_chat_id is None:
					update.message.reply_text(messages.BOT_NOT_STARTED)
					logger.warning(f'{curr_user} tried to contact their mortal but their mortal has not started this bot')
					return
				else:
					context.bot.send_photo(chat_id=mortal_chat_id, photo=image_id)
		except Exception as e:
			logger.error(f'{curr_user} failed to send a photo message')
			update.message.reply_text(messages.MESSAGE_SEND_FAIL)
	

def main() -> None:
	updater = Updater(BOT_TOKEN)

	# Get the dispatcher to register handlers
	dispatcher = updater.dispatcher

	# on different commands - answer in Telegram
	dispatcher.add_handler(CommandHandler("start", start))
	dispatcher.add_handler(CommandHandler("help", help_command))

	# dispatcher.add_handler(CommandHandler("generatetext", generate_text))

	dispatcher.add_handler(CommandHandler("revealmortal", reveal_mortal_command))
	dispatcher.add_handler(CallbackQueryHandler(reveal_mortal, pattern='reveal'))

	dispatcher.add_handler(CommandHandler("setrecipient", set_message_recipient))
	dispatcher.add_handler(CallbackQueryHandler(set_recipient_angel, pattern='angel'))
	dispatcher.add_handler(CallbackQueryHandler(set_recipient_mortal, pattern='mortal'))


	# on non command i.e message - send the message on Telegram to the user
	dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_message))
	dispatcher.add_handler(MessageHandler(Filters.photo & ~Filters.command, forward_photo_message))


	if HOST == "local":
		# Start the Bot
		updater.start_polling()
	elif HOST == "heroku":
		# Start the Bot on web host
		updater.start_webhook(listen="0.0.0.0",
							port=PORT,
							url_path=BOT_TOKEN,
							webhook_url=HEROKU_LINK + BOT_TOKEN)

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()

if __name__ == '__main__':
	main()
