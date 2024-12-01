import random
import time

from Card import Card
from Player import Player


class Game:
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.playersWhoCanMakeAccusation = player_names
        self.murder_solution = []
        self.deal_cards(len(self.players))

    def deal_cards(self, num_players):
        y = int(15 / num_players)
        count = y
        excess_cards = 15 % num_players
        temp_decs = []

        # Select one suspect, weapon, and room for the solution
        self.murder_solution = [
            random.choice(SUSPECTS),
            random.choice(WEAPONS),
            random.choice(ROOMS)
        ]
        print("DEBUG: Murder solution (hidden):", self.murder_solution)

        # Remove solution cards from deck
        deck = [Card(s) for s in SUSPECTS if s not in self.murder_solution]
        deck += [Card(w) for w in WEAPONS if w not in self.murder_solution]
        deck += [Card(r) for r in ROOMS if r not in self.murder_solution]

        random.shuffle(deck)
        # Deal remaining cards to players
        while deck:
            for player in self.players:
                if deck:
                    player.add_card(deck.pop())

        for player in self.players:
            player.update_possible_answer()

    def make_suggestion(self, player_name, suspect, weapon, room):
        print(f"{player_name} suggests: {suspect} with the {weapon} in the {room}")
        temp_win = True
        for player in self.players:
            if player.name != player_name:
                # Check if player can refute
                for card in player.hand:
                    if card.name in [suspect, weapon, room]:
                        print(f"{player_name} refutes with {card.name}")
                        temp_win = False
                        break
                if not temp_win:
                    break

        if temp_win:
            print(f"No proof against {player_name}'s suggestion.")

    def make_accusation(self, player_name, suspect, weapon, room):
        if [suspect, weapon, room] == self.murder_solution:
            print(f"{player_name} wins! The murder was committed by {suspect} with the {weapon} in the {room}!")
            return True
        else:
            print(f"{player_name} made a false accusation. Game continues.")
            self.playersWhoCanMakeAccusation.remove(player_name)
            return False

    def dice_s(self):
        return random.randint(1, 6)

    def show_player_deck_and_points(self):
        for player in game.players:
            cards = []
            for card in player.hand:
                cards.append(card.name)
            print(f"Player {player.name} Cards: {cards}\nYour points: {player.player_point}\n\n")

    def player_turn(self):
        win = False
        for player in game.players:
            print(f"{player.name} is rolling dice..")
            dice_count = game.dice_s()
            print(f"{player.name} has rolled dice {dice_count}")
            player.player_point += dice_count
            if player.player_point >= 8:
                print("Want to enter in a room ? (y/n)")
                choice = random.choices(['y', 'n'], weights=(98, 2))
                print(f"You have chosen {choice} to enter room")
                if 'y' in choice:
                    player.player_point = 0
                    room = player.choose_room()
                    suspect, weapon = player.choose_suspect_and_weapon()
                    game.make_suggestion(player.name, suspect, weapon, room)
                    if player.name in game.playersWhoCanMakeAccusation:
                        print("Do you want to reveal cards ?(y/n)")
                        choice_r = random.choices(['y', 'n'], weights=(50, 50))
                        print(f"You have chosen {choice_r} to reveal cards")
                        if 'y' in choice_r:
                            return game.make_accusation(player.name, suspect, weapon, room)
                        else:
                            pass
                else:
                    pass
        return False

if __name__ == '__main__':
    # Card categories
    SUSPECTS = ["Miss. Scarlett", "Colonel. Mustard", "Mrs. White", "Reverend. Green", "Mrs. Peacock", "Professor. Plum"]
    WEAPONS = ["Knife", "Candlestick", "Revolver", "Rope", "Lead pipe", "Wrench"]
    ROOMS = ["Hall", "Lounge", "Dining room", "Kitchen", "Ballroom", "Conservatory", "Billiard room", "Library", "Study"]

    # Example game setup with players
    player_names = ["Alice", "Bob", "Charlie"]
    game = Game(player_names)

    win = False
    while not win and len(game.playersWhoCanMakeAccusation) != 0:
        game.show_player_deck_and_points()
        time.sleep(1)
        win = game.player_turn()
        print("\n\n")

    if len(game.playersWhoCanMakeAccusation) == 0:
        print("All players have been eliminated from making accusations")
    print("Thanks for playing.")
