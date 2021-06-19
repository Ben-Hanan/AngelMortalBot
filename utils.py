import requests
from config import GOOGLE_SCRIPT

UPDATE_SUCCESSFUL = '200'
UPDATE_UNSUCCESSFUL = '404'

def getPlayersFromGoogleSheets():
	response = requests.get(GOOGLE_SCRIPT)
	players = response.json()
	return players

def updateGoogleSheetsPlayers(username, chat_id):
	try:
		parameters = { 'username': str(username).lower(), 'chat_id': str(chat_id) }
		response = requests.post(GOOGLE_SCRIPT, parameters)
		return response.json()
	except Exception as e:
		return e
