import socket
import random
import time

from Card import Card
from Player import Player


class CluedoGameServer:
    def __init__(self, ipaddress, names, n_players, suspects, weapons, rooms):
        self.n_players = n_players
        self.possible_names = names
        self.players = []
        self.members = {}
        self.playersWhoCanMakeAccusation = []
        self.murder_solution = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ipaddress, 55555))
        self.server.listen(n_players)
        self.suspect_options = """  
        ******************************************************************
        Suspects: Colonel. Mustard || Professor. Plum || Reverend. Green || Mrs. Peacock || Miss. Scarlett || Mrs. White
        ******************************************************************
        """
        self.weapon_options = """  
        ******************************************************************
        Weapons: Knife || Candlestick || Revolver || Rope || Lead pipe || Wrench
        ******************************************************************
        """
        self.room_options = """  
        ******************************************************************
        Rooms: 1. Hall || 2. Lounge || 3. Dining room || 4. Kitchen || 5. Ballroom || 6. Conservatory || 7. Billiard room || 8. Library || 9. Study
        ******************************************************************
        """
        self.suggestion = '''
        --------------
        | Killer: {} |
        | Weapon: {} |
        | Place : {} |
        -------------- 
        '''
        self.SUSPECTS = suspects
        self.WEAPONS = weapons
        self.ROOMS = rooms

    # Sends message to all players in the game.
    def send_all(self, message, ex_id=""):
        for player in self.players:
            if player.parameter == ex_id:
                continue
            player.parameter.send(message.encode("utf-8"))

    # Shuffle cards and distribute among players.
    # Returns two dicts: 1.) playername-their cards 2.) Murder Envelope cards.
    def deal_cards(self):
        num_players = len(self.players)
        # Select one suspect, weapon, and room for the solution
        self.murder_solution = [
            random.choice(self.SUSPECTS),
            random.choice(self.WEAPONS),
            random.choice(self.ROOMS)
        ]
        print("DEBUG: Murder solution (hidden):", self.murder_solution)

        # Remove solution cards from deck
        deck = [Card(s) for s in self.SUSPECTS if s not in self.murder_solution]
        deck += [Card(w) for w in self.WEAPONS if w not in self.murder_solution]
        deck += [Card(r) for r in self.ROOMS if r not in self.murder_solution]

        excess_cards = len(deck) % num_players
        count = len(deck) - excess_cards

        random.shuffle(deck)
        # Deal remaining cards to players
        deck = deck[0:count]
        while deck:
            for player in self.players:
                if deck:
                    player.add_card(deck.pop())

        for player in self.players:
            player.update_possible_answer()

    def add_player(self, player):
        """ Ask newly joined players to choose and name and checks if there is no same name collision."""
        possiblenames = iter(self.possible_names)
        name = next(possiblenames)
        while name in self.playersWhoCanMakeAccusation:
            name = next(possiblenames)
        self.playersWhoCanMakeAccusation.append(name)
        self.players.append(Player(name, player))
        return name

    def accept_requests(self):
        """Accepts new connection until selected number of people join."""
        game_welcome_text_1 = '''
        ******************************************************************
        Welcome to the classic detective game Cluedo!
        ******************************************************************
        '''
        game_welcome_text_2 = '''
        ******************************************************************
        Let the investigation begin...
        ******************************************************************
        '''
        while len(self.players) < self.n_players:
            self.send_all("Waiting for other players to join...")
            player, address = self.server.accept()
            name = self.add_player(player)
            self.send_all(f"{name} has joined the Game.\n")
        self.deal_cards()
        time.sleep(2)
        self.send_all("\nShuffling Cards...")
        time.sleep(2)
        self.send_all("...")
        time.sleep(2)
        self.send_all("...")
        time.sleep(2)
        self.send_all(game_welcome_text_1)
        time.sleep(2)
        self.send_all(game_welcome_text_2)
        time.sleep(2)
        self.playersWhoCanMakeAccusation.sort()
        self.main_game()
        return None

    def player_turn(self):
        """Ask the given player to roll dice and enter in room to make suggestion if applicable.
        returns True only when player wins."""
        win = False
        for player in self.players:
            player_id = player.parameter
            name = player.name
            temp_win = True
            player_id.send("******************************************************************\n".encode("utf-8"))
            player_id.send("Hit 'y' to Roll Dice..".encode("utf-8"))
            player_id.recv(1024).decode("utf-8")
            dice_count = random.randint(1, 6)
            player_id.send("\n******************************************************************".encode("utf-8"))
            player_id.send(f"You have rolled: {dice_count}.".encode("utf-8"))
            self.send_all(f"{name} rolled: {dice_count}", ex_id=player_id)
            player.player_point += dice_count
            if player.player_point >= 8:
                player_id.send("\nWant to enter in a room ? (y/n)".encode("utf-8"))
                choice = player_id.recv(1024).decode("utf-8")
                if choice == 'y':
                    player.player_point = 0

                    player_id.send(self.room_options.encode("utf-8"))
                    player_id.send("\nChoose a room to enter: ".encode("utf-8"))
                    room = player_id.recv(1024).decode("utf-8")
                    while room not in self.ROOMS:  # Check if entered option is valid.
                        player_id.send("Invalid room selected!\n".encode("utf-8"))
                        print(f"Invalid Character Entered by user")
                        room = player_id.recv(1024).decode("utf-8")

                    player_id.send("\nChoose a Suspect".encode("utf-8"))
                    time.sleep(0.5)
                    player_id.send(self.suspect_options.encode("utf-8"))
                    suspect = player_id.recv(1024).decode("utf-8")
                    while suspect not in self.SUSPECTS:
                        print(f"Invalid Character Entered")
                        player_id.send("Invalid Character selected!".encode("utf-8"))
                        time.sleep(0.5)
                        suspect = player_id.recv(1024).decode("utf-8")

                    player_id.send("\nChoose a Weapon".encode("utf-8"))
                    time.sleep(0.5)
                    player_id.send(self.weapon_options.encode("utf-8"))
                    weapon = player_id.recv(1024).decode("utf-8")
                    while weapon not in self.WEAPONS:
                        print(f"Invalid Weapon Entered")
                        player_id.send("Invalid Character selected!".encode("utf-8"))
                        weapon = player_id.recv(1024).decode("utf-8")

                    self.send_all(f"\n{name}'s suggestion:")
                    self.send_all(self.suggestion.format(suspect, weapon, room))
                    accused = [suspect, weapon, room]
                    time.sleep(2)

                    winning = self.make_suggestion(player, suspect, weapon, room)

                    if name in self.playersWhoCanMakeAccusation:
                        player_id.send("Do you want to revel cards ?(y/n)".encode("utf-8"))
                        choice_r = player_id.recv(1024).decode("utf-8")
                        if choice_r == 'y':
                            return self.make_accusation(name, suspect, weapon, room)
                        else:
                            pass
                else:
                    pass
        return False

    def make_suggestion(self, p, suspect, weapon, room):
        print(f"{p.name} suggests: {suspect} with the {weapon} in the {room}")
        temp_win = True
        accused = [suspect, weapon, room]
        for player in self.players:
            for accuse in accused:
                for card in player.hand:
                    if accuse in card.name and player.name != p.name:
                        print(f"{player.name} has disapproved {p.name}'s suggestion.")
                        p.possible_answer.remove(accuse)
                        temp_win = False
                        break
                if not temp_win:
                    break
            if not temp_win:
                break

        if temp_win:
            print(f"No proof against {p.name}'s suggestion.")
        return temp_win

    def make_accusation(self, player_name, suspect, weapon, room):
        if [suspect, weapon, room] == self.murder_solution:
            self.send_all(f"{player_name} WON !")
            print(f"{player_name} wins! The murder was committed by {suspect} with the {weapon} in the {room}!")
            return True
        else:
            print(f"{player_name} made a false accusation. Game continues.")
            self.send_all(f"Wrong accusation !\n{player_name} will no longer make accusations.")
            self.playersWhoCanMakeAccusation.remove(player_name)
            return False

    # Display each player their cards and points.
    def display_player_deck_and_points(self):
        for player in self.players:
            player_id = player.parameter
            point = player.player_point
            deck = [card.name for card in player.hand]
            player_id.send("\n******************************************************************\n".encode("utf-8"))
            player_id.send(f"Your Cards: {deck}\nYour points: {point}\n\n".encode("utf-8"))

    def main_game(self):
        """Passes player name to 'player_turn' function turn-by-turn until one player wins."""
        win = False
        while not win and len(self.playersWhoCanMakeAccusation) != 0:
            self.display_player_deck_and_points()
            time.sleep(1)
            win = self.player_turn()
            print("\n\n")

        if len(self.playersWhoCanMakeAccusation) == 0:
            self.send_all("All players have been removed from making accusations")

        self.send_all("Thanks for playing.")
        self.server.close()
