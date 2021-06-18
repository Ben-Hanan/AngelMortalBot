import requests
from config import GOOGLE_SCRIPT

def getPlayers():
	response = requests.get(GOOGLE_SCRIPT)
	players = response.json()
	return players

def updatePlayers(username, user_id):
	params = { 'username': str(username), 'chat_id': str(user_id) }
	response = requests.post(GOOGLE_SCRIPT, params)
	output = response.json()
	return output
