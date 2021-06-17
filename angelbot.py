#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

import logging
import messages

from config import ANGEL_BOT_TOKEN

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    
    print(user.id, user.username)

    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

"""
def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)
"""

def forward_message(update: Update, context: CallbackContext) -> None:
    """Send a message to either the Angel or Mortal depending on the mode set"""
    if players[players[curr_user].angel].chat_id is None:
        update.message.reply_text(messages.BOT_NOT_STARTED)
        return ConversationHandler.END
    update.message.reply_text(update.message.text)

def set_texting_angel(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    curr_user = user.username

    if (players[curr_user].is_texting_angel is True):
        update.message.reply_text(messages.ALREADY_TEXTING_ANGEL)
    else:
        players[curr_user].is_texting_angel = True
        update.message.reply_text(messages.SET_TEXTING_ANGEL)

def set_texting_mortal(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    curr_user = user.username

    if (players[curr_user].is_texting_angel is False):
        update.message.reply_text(messages.ALREADY_TEXTING_MORTAL)
    else:
        players[curr_user].is_texting_angel = False
        update.message.reply_text(messages.SET_TEXTING_MORTAL)

def main() -> None:
    updater = Updater(ANGEL_BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("Send", send_command))
    dispatcher.add_handler(CommandHandler("text_angel", set_texting_angel))
    dispatcher.add_handler(CommandHandler("text_mortal", set_texting_mortal))

    # on non command i.e message - send the message on Telegram to the user
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, forward_message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()