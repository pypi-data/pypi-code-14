#!/usr/bin/env python3 -tt
"""
File: lol_sync.py
-----------------
@author Jason Lin, jason0@stanford.edu

Notifies you when your friends are finished with their League of Legends game
and are ready to play!
"""
import requests
import time
import calendar
from blessings import Terminal
import os
import subprocess

term = Terminal()


def main():
	""" Prompts user for a username to track.

	Continues to prompt until a valid username is given, then calls the
	check_in_game function to check when the user finishes their game.
	"""
	user_id = None
	username = input("Please enter the username of friend to track ('q' to quit): ")
	if username == "q":
		quit()
	user_id = find_id(username)
	while user_id is None:
		username = input("Invalid username. Please try again: ")
		user_id = find_id(username)
	print("Tracking user " + username + "...")
	check_in_game(user_id, username)


def print_time(game_length, seconds):
	""" Helper function to print the game time

	Prints the formatted game time in Minutes:Seconds format.
	Then increments game time and sleeps for one second, finally
	erasing the previous time just before printing the next time
	to emulate a timer.
	"""
	for second in range(seconds):
		print("In game for: " + time.strftime('%M:%S', time.localtime(game_length)), end="\r")
		game_length += 1
		time.sleep(1)
		print(term.clear_eol, end='')


def get_game_info(user_id):
	""" Helper function to make an API GET request for the current game information.

	Parameters include the user id of the entered username and the API key.
	"""
	return requests.get('http://52.89.79.213/game/' + str(user_id))


def get_champ_name(game_data, username):
	""" Function to retrieve the name of the champion that the user is currently playing.

	Gets the list of game participants from the current game request, then searches through it to find
	the correct participant (the entered username). Finally, makes a GET request to the API to find
	the correct champion name that corresponds to the champion id that is returned.
	"""
	game_participants = game_data.get('participants')
	champ_id = 0
	for player in game_participants:
		if player.get('summonerName').lower() == username:
			champ_id = player.get('championId')
	champ_request = requests.get('http://52.89.79.213/champion/' + str(champ_id))
	champ_data = champ_request.json()
	return champ_data.get('name')


def check_in_game(user_id, username):
	"""	Checks whether the user is in game.

	If the current game request is valid, then continuously makes a request until the game is not found.
	Then notifies the user through a desktop notification that the game has been finished.
	"""
	r = get_game_info(user_id)
	if not r.ok:
		print("User " + username + " is not currently in a game. Start one up now!")
	else:
		game_data = r.json()
		game_start = game_data.get('gameStartTime')/1000
		game_length = calendar.timegm(time.gmtime()) - game_start
		champion = get_champ_name(game_data, username)
		os.system('clear')
		print("User " + username + " is in game, currently playing " + champion + "!")
		print("Game started at: ", end="")
		print(time.strftime('%l:%M%p %Z on %b %d, %Y', time.localtime(game_start)))
		while r.status_code != 404:
			print_time(game_length, 3)
			game_length += 3
			r = get_game_info(user_id)
		print("User " + username + " just finished their game. Start one up now!")
		try:
			subprocess.call(["terminal-notifier", "-title", username + " finished their game!", "-message", "Start one up now!"])
		except:
			pass
	main()


def find_id(username):
	""" Finds the user id of a given username.

	Makes an API GET request to find the unique user id for a given username,
	and returns None if not found.
	"""
	r = requests.get('http://52.89.79.213/username/' + username)
	if r.ok:
		data = r.json()
		username = username.replace(" ", "")
		return data.get(username).get('id')
	else:
		return None

main()
