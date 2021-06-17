from config import PLAYERS_FILENAME

class Player():
	def __init__(self):
		self.username = None
		self.angel = None
		self.mortal = None
		self.chat_id = None
		self.is_texting_angel = None
	
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