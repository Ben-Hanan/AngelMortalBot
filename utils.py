import requests
from config import GOOGLE_SCRIPT

def getPlayersFromGoogleSheets():
	response = requests.get(GOOGLE_SCRIPT)
	players = response.json()
	return players

def updateGoogleSheetsPlayers(username, user_id):
	params = { 'username': str(username).lower(), 'chat_id': str(user_id) }
	response = requests.post(GOOGLE_SCRIPT, params)
	output = response.json()
	return output
