import random


class Player:
    def __init__(self, name, parameter=None):
        self.name = name
        self.hand = []
        self.player_point = 0
        self.possible_answer = ["Miss. Scarlett", "Colonel. Mustard", "Mrs. White", "Reverend. Green", "Mrs. Peacock",
                                "Professor. Plum",
                                "Knife", "Candlestick", "Revolver", "Rope", "Lead pipe", "Wrench",
                                "Hall", "Lounge", "Dining room", "Kitchen", "Ballroom", "Conservatory", "Billiard room",
                                "Library", "Study"]

        self.rooms = ["Hall", "Lounge", "Dining room", "Kitchen", "Ballroom", "Conservatory", "Billiard room",
                      "Library", "Study"]

        self.suspects = ["Miss. Scarlett", "Colonel. Mustard", "Mrs. White", "Reverend. Green", "Mrs. Peacock",
                         "Professor. Plum"]

        self.weapon = ["Knife", "Candlestick", "Revolver", "Rope", "Lead pipe", "Wrench"]
        self.parameter = parameter

    def add_card(self, card):
        self.hand.append(card)

    def update_possible_answer(self):
        for card in self.hand:
            if card.name in self.possible_answer:
                self.possible_answer.remove(card.name)

    def __str__(self):
        return self.name

    def choose_suspect_and_weapon(self):
        found = False
        while found is False:
            suspect = random.choice(self.suspects)
            if suspect in self.possible_answer:
                found = True
                break
            else:
                pass

        found = False
        while found is False:
            weapon = random.choice(self.weapon)
            if weapon in self.possible_answer:
                found = True
                break
        return suspect, weapon

    def choose_room(self):
        found = False
        while found is False:
            room = random.choice(self.rooms)
            if room in self.possible_answer:
                found = True
                break
        return room
