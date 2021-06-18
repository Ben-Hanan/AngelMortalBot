from config import PLAYERS_FILENAME

class Player():
	def __init__(self, username, angel, mortal, chat_id):
		self.username = username
		self.angel = angel
		self.mortal = mortal
		self.chat_id = chat_id
		self.is_recipient_angel = None
	
def initialize_players(players_obj):
	players_file = open(PLAYERS_FILENAME, "r")	
	all_players = players_file.readlines()

	for line in all_players:
		data = line.split(",")	
		username = data[0].strip().lower()
		angel = data[1].strip().lower()
		mortal = data[2].strip().lower()

		try:
			# If chat_id is already stored on the .txt file, add it to the player profile
			chat_id = data[3].strip().lower()
			players_obj[username] = Player(username, angel, mortal, chat_id)

		except:
			players_obj[username] = Player(username, angel, mortal, None)