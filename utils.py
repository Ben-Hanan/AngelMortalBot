import requests
from config import GOOGLE_SCRIPT, OPEN_AI

UPDATE_SUCCESSFUL = '200'
UPDATE_UNSUCCESSFUL = '404'

open_ai_endpoint = "https://api.openai.com/v1/completions"
model_engine = "text-davinci-002"

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

def promptAi(prompt):
	payload = {	"model": model_engine,
				"prompt": prompt,
				"max_tokens": 200,
				"n": 1,
				"stop": "?|.",
				"temperature": 0.7,
				"presence_penalty" : 0.5 }

	response = requests.post(open_ai_endpoint, json=payload, headers={"Authorization": f"Bearer {OPEN_AI}"})
	print(response.json())
	return response.json()["choices"][0]["text"]
