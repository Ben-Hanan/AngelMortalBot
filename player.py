from utils import getPlayersFromGoogleSheets

class Player():
	def __init__(self):
		self.username = None
		self.angel = None
		self.mortal = None
		self.chat_id = None
		self.is_recipient_angel = None
	
def initialize_players(players_obj):
	all_players = getPlayersFromGoogleSheets()

	for line in all_players:
		username = line["user"].lower()
		angel = line["angel"].lower()
		mortal = line["mortal"].lower()
		chat_id = line["chat_id"]

		players_obj[username].username = username
		players_obj[username].angel = players_obj[angel]
		players_obj[username].mortal = players_obj[mortal]

		if chat_id:
			players_obj[username].chat_id = chat_id