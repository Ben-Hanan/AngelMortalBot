from utils import getPlayersFromGoogleSheets
from collections import defaultdict
import random

class Player():
	def __init__(self):
		self.username = None
		self.angel = None
		self.mortal = None
		self.chat_id = None
		self.vg = None
		self.is_recipient_angel = None
	
	def __repr__(self) -> str:
		return f"u:{self.username} | a:{self.angel} | m:{self.mortal} | vg:{self.vg} | {self.chat_id}"
	
def initialize_players(players_obj):
	all_players = getPlayersFromGoogleSheets()

	for line in all_players:
		username = str(line["user"]).strip().lower()
		angel = line["angel"].strip().lower()
		mortal = line["mortal"].strip().lower()
		vg = line["vg"].strip().lower()
		chat_id = line["chat_id"]

		players_obj[username].username = username
		players_obj[username].angel = players_obj[angel]
		players_obj[username].mortal = players_obj[mortal]
		players_obj[username].vg = vg

		if chat_id:
			players_obj[username].chat_id = chat_id

def choose_vg(lst, exception):
	possible_choices = [v for v in lst if v != exception]
	if possible_choices:
		return random.choice(possible_choices)
	else:
		return None

def choose_mortal(lst):
	possible_choices = [v for v in lst if v.angel is None]
	if possible_choices:
		return random.choice(possible_choices)
	else:
		return None

def randomizePairings():
	players = defaultdict(Player)
	initialize_players(players)

	player_vg = defaultdict(list)

	for player in players.values():
		player_vg[player.vg].append(player)

	del player_vg[None]
	vg_list = list(player_vg.keys())
	print(vg_list)

	idx = 0
	curr_player = list(players.values())[0]
	while idx < len(list(players.keys())):
		mortal_vg = choose_vg(vg_list, curr_player.vg)
		if mortal_vg is None:
			print("no more vgs")
			break
		mortal = choose_mortal(player_vg[mortal_vg])
		# If mortal cannot be found, remove filled VG and continue
		if mortal is None:
			print(f"vg has no more youths to be an angel for, removing {mortal_vg}")
			vg_list.remove(mortal_vg)
			continue
		mortal_username = mortal.username
		curr_player.mortal = mortal_username
		players[mortal_username].angel = curr_player.username
		curr_player = mortal
		idx += 1
	
	with open("pairings.csv", "w") as f:
		for player in players.values():
			f.write(f"{player.username}, {player.angel}, {player.mortal}, {player.vg}, {player.chat_id}\n")

if __name__ == '__main__':
	randomizePairings()