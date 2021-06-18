import logging
import time
import messages
import player
from collections import defaultdict

from config import BOT_TOKEN, PLAYERS_FILENAME, HOST, PORT, APP_NAME

from telegram import Update, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, InlineQueryHandler, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
players = defaultdict(player.Player)
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

# TODO: Update welcome message
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user

    updatePlayerProfile(user.id, user.username)

    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!'
        + messages.START_MESSAGE,
        reply_markup=ForceReply(selective=True),
    )

def reveal_mortal_command(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    mortal = players[user.username].mortal

    if mortal is None:
        update.message.reply_text(messages.MORTAL_NOT_FOUND)
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
    mortal = players[user.username].mortal

    context.bot.answerCallbackQuery(
        callback_query_id=update.callback_query.id, 
        text=messages.format_mortal_reveal(mortal),
    )

#TODO: Update help command
def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(messages.format_help_message())

def forward_message(update: Update, context: CallbackContext) -> None:
    """Send a message to either the Angel or Mortal depending on the mode set"""
    user = update.effective_user
    curr_user = user.username.lower()

    if players[curr_user].is_recipient_angel is None:
        update.message.reply_text(messages.CHOOSE_RECIPIENT)
    else:
        if players[curr_user].is_recipient_angel is True:
            angel_chat_id = players[curr_user].angel.chat_id
            if angel_chat_id is None:
                update.callback_query.message.edit_text(messages.BOT_NOT_STARTED)
                return
            else:
                context.bot.send_message(
                    text=messages.format_mortal_message(update.message.text),
                    chat_id=angel_chat_id
                )
        
        if players[curr_user].is_recipient_angel is False:
            mortal_chat_id = players[curr_user].mortal.chat_id
            if mortal_chat_id is None:
                update.callback_query.message.edit_text(messages.BOT_NOT_STARTED)
                return
            else:
                context.bot.send_message(
                    text=messages.format_angel_message(update.message.text),
                    chat_id=mortal_chat_id
                )

def set_recipient_angel(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    curr_user = user.username.lower()

    if (players[curr_user].is_recipient_angel is True):
        update.message.reply_text(messages.ALREADY_TEXTING_ANGEL)
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
        update.message.reply_text(text=messages.ALREADY_TEXTING_MORTAL)
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

def main() -> None:
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(CommandHandler("revealmortal", reveal_mortal_command))
    dispatcher.add_handler(CallbackQueryHandler(reveal_mortal, pattern='reveal'))

    dispatcher.add_handler(CommandHandler("setrecipient", set_message_recipient))
    dispatcher.add_handler(CallbackQueryHandler(set_recipient_angel, pattern='angel'))
    dispatcher.add_handler(CallbackQueryHandler(set_recipient_mortal, pattern='mortal'))


    # on non command i.e message - send the message on Telegram to the user
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_message))


    if HOST == "local":
        # Start the Bot
        updater.start_polling()
    elif HOST == "heroku":
        # Start the Bot on web host
        updater.start_webhook(listen="0.0.0.0",
                            port=PORT,
                            url_path=BOT_TOKEN,
                            webhook_url="https://" + APP_NAME + ".herokuapp.com/" + BOT_TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()