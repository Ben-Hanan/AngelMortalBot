HELP = f'Placeholder text'
NOT_INITIALIZED = f'Sorry! But it looks like you are not in this round of angel-mortal! If this is a mistake please contact the admin with @HananChoong or @hansebeast'
SET_MESSAGING_ANGEL = f'You are now chatting with your Angel!'
SET_MESSAGING_MORTAL = f'You are now chatting with your Mortal!'
BOT_NOT_STARTED = f'The player you are trying to chat with has not started this bot'
ALREADY_TEXTING_MORTAL = f'You are already chatting with your Mortal!'
ALREADY_TEXTING_ANGEL = f'You are already chatting with your Angel!'
CHOOSE_RECIPIENT = f'Please select who you want to send this message to through the use of the command /setrecipient'

CHATTING_WITH_ANGEL= '\U0001F47C\U0001F3FC' + " You are now chatting with your Angel " + '\U0001F47C\U0001F3FC'
CHATTING_WITH_MORTAL = '\U0001F466\U0001F3FC' + "You are now chatting with your Mortal " + '\U0001F467\U0001F3FC'

# TODO: format messages nicer
def format_mortal_message(message):
    return 'From your mortal:\n' + message

def format_mortal_angel(message):
    return 'From your angel:\n' + message