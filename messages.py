CONTACT = f'contact either the admin @ednaleong or the creators of this bot @hansebeast and @HananChoong'

NOT_INITIALIZED = f'\n\nSorry\! But it looks like you are not in this round of angel mortal\! If this is a mistake please ' + CONTACT
BOT_NOT_STARTED = f'The player you are trying to chat with has not started this bot. Please wait for them to start the bot. If this is unexpected please ' + CONTACT
MORTAL_NOT_FOUND = f"You don't have a mortal! If this is wrong, please " + CONTACT
ALREADY_TEXTING_MORTAL = '\U0001F466\U0001F3FC' + f'You are chatting with your Mortal!' + '\U0001F467\U0001F3FC'
ALREADY_TEXTING_ANGEL = '\U0001F47C\U0001F3FC' + f'You are chatting with your Angel!' + '\U0001F47C\U0001F3FC'

CHOOSE_RECIPIENT = f'Please select who you want to send this message to through the use of the command /setrecipient'
CHATTING_WITH_ANGEL= '\U0001F47C\U0001F3FC' + " You are now chatting with your Angel " + '\U0001F47C\U0001F3FC'
CHATTING_WITH_MORTAL= '\U0001F466\U0001F3FC' + " You are now chatting with your Mortal " + '\U0001F467\U0001F3FC'

START_MESSAGE = f'\n\nWelcome to Angel Mortal, a game where you try to be the best angel to your mortal by showering them with love ' + '\U0001F60D' + '\n\n'
TUTORIAL = f'Since the aim of the game is to love on one another ' + '\u2764 ' + 'but remain anonymous ' + '\U0001F464' + ' at the same time, you can use me to relay your messages to both you angel and your mortal\! Isn\'t that convenient\!\n\n'
EXAMPLES = f'Some examples of what you can do could be:\nSending them a prayer/words of encouragement\nyou can ask for their address and buy them food\!\nchat with them\n\n'
END_START = f'If you need any help, you can bring up the help message through /help and if you\'re ready to start, you can find out who your mortal is by typing /revealmortal \n\n Have a blessed V Camp\!'

HELP_MESSAGE = f'I am the middleman between you and your mortal or angel.\n\n' + f'You can control who you talk to using this command:\n\n'
COMMAND = f'/setrecipient : choose to send messages to either your angel or mortal\n' + '/revealmortal : reveal your mortal to you!\n\n'
LIMITATIONS = f'Keep in mind that in the current implementation of this bot, I am unable to forward any forms of media ' + '\U0001F62A' + '\n\n'
ASSISTANCE = f'If you ever need more assistance, you can ' + CONTACT

# TODO: format messages nicer
def format_mortal_message(message):
    return 'From your mortal:\n' + message

def format_angel_message(message):
    return 'From your angel:\n' + message

def format_start_message():
    return START_MESSAGE + TUTORIAL + EXAMPLES + END_START

def format_help_message():
    return HELP_MESSAGE + COMMAND + LIMITATIONS + ASSISTANCE

def format_mortal_reveal(mortal):
    return f'Your mortal is {mortal.username}!\n\n' + f'Please do your best to take care of {mortal.username} and ensure that they feel loved during the duration of this game!' + '\u2764'