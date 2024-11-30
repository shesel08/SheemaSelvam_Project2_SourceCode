import socket
import re
import random
import sys
import time
import itertools

players = []
playernames = []
members = {}
players_deck = {}
player_point = {}
murder_solution = {}
valid_name_pattern = r'[A-Za-z0-9-_]*'
game_art1 = '''
==================================================================
Welcome to the classic detective game: 
==================================================================
'''
game_art2 = '''
 .d8888b.     888                                 888              
d88P  Y88b    888                                 888              
888    888    888                                 888             
888           888    888  888     .d88b.      .d88888     .d88b.  
888           888    888  888    d8P  Y8b    d88" 888    d88""88b 
888    888    888    888  888    88888888    888  888    888  888 
Y88b  d88P    888    Y88b 888    Y8b.        Y88b 888    Y88..88P 
 "Y8888P"     888     "Y88888     "Y8888      "Y88888     "Y88P" 
 '''
game_art3 = '''
==================================================================
Let the investigation begin...
==================================================================
 
'''
option_table = """  
================================================
||........Suspects.......||......Weapons......||
||  1.) Colonel Mustard  ||  1.) Knife        ||
||  2.) Professor Plum   ||  2.) Candlestick  ||
||  3.) Reverend Green   ||  3.) Revolver     ||
||  4.) Mrs. Peacock     ||  4.) Rope         ||
||  5.) Miss Scarlett    ||  5.) Lead pipe    ||
||  6.) Mrs. White       ||  6.) Wrench       ||
================================================
"""
room_table = """  
=========================
||........Rooms........||
||  1.) Hall           ||
||  2.) Lounge         ||
||  3.) Dining room    ||
||  4.) Kitchen        ||
||  5.) Ballroom       ||
||  6.) Conservatory   ||
||  7.) Billiard room  ||
||  8.) Library        ||
||  9.) Study          ||
=========================
"""
suggestion = '''
--------------
| Killer: {} |
| Weapon: {} |
| Place : {} |
-------------- 
'''

SUSPECTS = {1: "Miss. Scarlett", 2: "Colonel. Mustard", 3: "Mrs. White", 4: "Reverend. Green", 5: "Mrs. Peacock",
            6: "Professor. Plum"}

WEAPONS = {1: "Knife", 2: "Candlestick", 3: "Revolver", 4: "Rope", 5: "Lead pipe", 6: "Wrench"}

ROOMS = {1: "Hall", 2: "Lounge", 3: "Dining room", 4: "Kitchen", 5: "Ballroom", 6: "Conservatory", 7: "Billiard room",
         8: "Library", 9: "Study"}

server_type = "127.0.0.1"  # Local host IP address.

n_players = int(input("Enter the number of players (2-6)\n(Least 3 players are recommended)\n"))
if type(n_players) == int and 6 >= n_players >= 3:
    print("Waiting for players to join....")
else:
    print("Invalid character entered.")
    sys.exit(1)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_type, 55555))
server.listen(n_players)


# Sends message to all players in the game.
def send_all(message, ex_id=""):
    for player in players:
        if player == ex_id:
            continue
        player.send(message.encode("utf-8"))


# Dice simulator.
def dice_s():
    return random.randint(1, 6)


# Shuffle cards and distribute among players. Returns two dicts: 1.) playername-their cards 2.) Murder Envelope cards.
def deal_cards(num_players, players_nicknames):
    x = 0
    y = int(15 / num_players)
    count = y
    excess_cards = 15 % num_players
    temp_decs = []
    deck = []
    # Select one suspect, weapon, and room for the solution
    murder_solution = dict(Killer=random.choice(list(SUSPECTS.values())), Weapon=random.choice(list(WEAPONS.values())),
                           Place=random.choice(list(ROOMS.values())))

    print("Murder solution:", murder_solution)
    # Remove solution cards from deck
    deck = [SUSPECTS[s] for s in SUSPECTS if SUSPECTS[s] not in murder_solution['Killer']]
    deck += [WEAPONS[w] for w in WEAPONS if WEAPONS[w] not in murder_solution['Weapon']]
    deck += [ROOMS[r] for r in ROOMS if ROOMS[r] not in murder_solution['Place']]

    random.shuffle(deck)
    for i in range(0, num_players):
        dec = deck[x:count]
        temp_decs.append(dec)
        x = count
        count += y
    count = 15 - excess_cards
    if excess_cards != 0:
        for i in range(1, excess_cards + 1):
            temp_decs[i].append(deck[count + i - 1])
    decks = {}
    for i in range(0, num_players):
        decks.update({players_nicknames[i]: temp_decs[i]})
    print(decks)
    return decks, murder_solution


def player_name(player):
    """ Ask newly joined players to choose and name and checks if there is no same name collision."""
    possiblenames = iter(['Bot-01', 'Bot-02', 'Bot-03', 'Bot-04', 'Bot-05', 'Bot-06'])
    name = next(possiblenames)
    while True:
        if re.fullmatch(valid_name_pattern, name):
            break
        else:
            name = next(possiblenames)
    while name in playernames:
        name = next(possiblenames)
    playernames.append(name)
    members.update({name: player})
    player_point.update({name: 0})
    return name


def accept_requests():
    """Accepts new connection until selected number of people join."""
    global players_deck, murder_solution
    while len(players) < n_players:
        send_all("Waiting for other players to join...")
        player, address = server.accept()
        players.append(player)
        name = player_name(player)
        send_all(f"{name} has joined the Game.\n")
    players_deck, murder_solution = deal_cards(n_players, playernames)
    time.sleep(2)
    send_all("\nShuffling Cards...")
    time.sleep(2)
    send_all("...")
    time.sleep(2)
    send_all("...")
    time.sleep(2)
    send_all(game_art1)
    time.sleep(2)
    send_all(game_art2)
    time.sleep(2)
    send_all(game_art3)
    time.sleep(2)
    playernames.sort()
    main_game()
    return None


def player_turn(name):
    """Ask the given player to roll dice and enter in room to make suggestion if applicable.
    returns True only when player wins."""
    player_id = members[name]
    temp_win = True
    player_id.send("---------------------------------------------------\n".encode("utf-8"))
    player_id.send("Hit 'y' to Roll Dice..".encode("utf-8"))
    player_id.recv(1024).decode("utf-8")
    dice_count = dice_s()
    player_id.send("\n=============================================".encode("utf-8"))
    player_id.send(f"You have rolled: {dice_count}.".encode("utf-8"))
    send_all(f"{name} rolled: {dice_count}", ex_id=player_id)
    player_point[name] += dice_count
    if player_point[name] >= 8:
        player_id.send("\nWant to enter in a room ? (y/n)".encode("utf-8"))
        choice = player_id.recv(1024).decode("utf-8")
        if choice == 'y':
            player_point[name] = 0
            player_id.send(room_table.encode("utf-8"))
            player_id.send("\nChoose a room to enter: ".encode("utf-8"))
            room_no = 0
            while room_no > 9 or room_no < 1 or type(room_no) != int:  # Check if entered option is valid.
                try:
                    room_no = int(player_id.recv(1024).decode("utf-8"))
                except Exception as e:
                    player_id.send("Invalid room selected!\n".encode("utf-8"))
                    print(f"Invalid Character Entered by user: {e}")
                    room_no = 0
            player_id.send("\nChoose Suspect and Weapon. (separated by space)".encode("utf-8"))
            time.sleep(0.5)
            player_id.send(option_table.encode("utf-8"))
            suspect_weapon = [0, 0]
            while suspect_weapon[0] > 6 or suspect_weapon[0] < 1 or type(suspect_weapon[0]) != int or len(
                    suspect_weapon) != 2:
                # Check if entered option is valid.
                try:
                    suspect_weapon = list(map(int, player_id.recv(1024).decode("utf-8").split(" ")))
                except Exception as er:
                    print(f"Invalid Character Entered: {er}")
                    player_id.send("Invalid Character selected!".encode("utf-8"))
                    suspect_weapon = [0, 0]
            while suspect_weapon[1] > 6 or suspect_weapon[1] < 1 or type(suspect_weapon[1]) != int or len(
                    suspect_weapon) != 2:
                # ..................................................................To check if entered option is valid.
                try:
                    suspect_weapon = list(map(int, player_id.recv(1024).decode("utf-8").split(" ")))
                except Exception as er:
                    print(f"Invalid Weapon Entered: {er}")
                    player_id.send("Invalid Character selected!".encode("utf-8"))
                    suspect_weapon = [0, 0]
            send_all(f"\n{name}'s suggestion:")
            send_all(suggestion.format((SUSPECTS[suspect_weapon[0]]), WEAPONS[suspect_weapon[1]], ROOMS[room_no]))
            accused = [SUSPECTS[suspect_weapon[0]], WEAPONS[suspect_weapon[1]], ROOMS[room_no]]
            time.sleep(2)
            for name in playernames:
                for accuse in accused:
                    if accuse in players_deck[name] and name != name:
                        send_all(f"{name} has disapproved {name}'s suggestion.", player_id)
                        player_id.send(f"{name} has {accuse}.".encode("utf-8"))
                        temp_win = False
                        break
                if not temp_win:
                    break
            if temp_win:
                send_all(f"No proof against {name}'s suggestion.")
            player_id.send("Do you want to revel cards ?(y/n)".encode("utf-8"))
            choice_r = player_id.recv(1024).decode("utf-8")
            if choice_r == 'y':
                if (murder_solution['Killer'] == SUSPECTS[suspect_weapon[0]]
                        and murder_solution['Weapon'] == WEAPONS[suspect_weapon[1]]
                        and murder_solution['Place'] == ROOMS[room_no]):
                    send_all(f"{name} WON !")
                    player_id.send(f"\nCongrats {name}, you have solved the case !".encode("utf-8"))
                    return True
                else:
                    send_all(f"Wrong accusation !\n{name} will no longer make accusations.")
                    try:
                        playernames.remove(name)
                    except ValueError:
                        print(f"{name} not found in the list.")
                        return None
            else:
                pass
        else:
            pass
    return False


# Display each player their cards and points.
def show_player_deck_and_points():
    for name in playernames:
        player_id = members[name]
        point = player_point[name]
        deck = players_deck[name]
        player_id.send("\n=============================================\n".encode("utf-8"))
        player_id.send(f"Your Cards: {deck}\nYour points: {point}\n\n".encode("utf-8"))


def main_game():
    """Passes player name to 'player_turn' function turn-by-turn until one player wins."""
    iter_nickname = itertools.cycle(playernames)
    name = next(iter_nickname)
    win = False
    while not win:
        time.sleep(1)
        show_player_deck_and_points()
        time.sleep(1)
        win = player_turn(name)
        if win is None:
            name = ""
            break
        name = next(iter_nickname)
    send_all("\nThanks for playing.")
    try:
        if len(playernames) != 0 and name in playernames:
            members.get(name).recv(1024).decode("utf-8")
    except Exception as e:
        print(e)
    server.close()


accept_requests()
