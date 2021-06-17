from config import PLAYERS_FILENAME

class Player():
	# username refers to the Telegram handle of the user.
	# angel, and mortal are Telegram handles of the angel and mortal of the user respectively.
	# chat_id is the id related to the username in Telegram
	def __init__(self, username, angel, mortal, chat_id):
		self.username = username 
		self.angel = angel 
		self.mortal = mortal
		self.chat_id = chat_id
	
def initialize_players(players_obj):
	players_file = open(PLAYERS_FILENAME, "r")	
	all_players = players_file.readlines()

	for idx, line in enumerate(all_players):
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