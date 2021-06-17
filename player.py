from config import PLAYERS_FILENAME

class Player():
	def __init__(self):
		self.username = None
		self.angel = None
		self.mortal = None
		self.chat_id = None
	
def initializePlayers():
		with open(PLAYERS_FILENAME)