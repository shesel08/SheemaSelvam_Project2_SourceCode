import re
import socket
import threading
import random
import time

initialised = False
pattern_1 = r'([A-Za-z0-9-_]*) has ([A-Za-z .]*).'
winning = False


class Player:
    def __init__(self, ip):
        self.host = ip
        self.user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user_socket.connect((self.host, 55555))

        # Possible Choices
        self.possible_answer = ["Miss. Scarlett", "Colonel. Mustard", "Mrs. White", "Reverend. Green", "Mrs. Peacock", "Professor. Plum",
                                "Knife", "Candlestick", "Revolver", "Rope", "Lead pipe", "Wrench",
                                "Hall", "Lounge", "Dining room", "Kitchen", "Ballroom", "Conservatory", "Billiard room", "Library", "Study"]

        self.rooms = {1: "Hall", 2: "Lounge", 3: "Dining room", 4: "Kitchen", 5: "Ballroom", 6: "Conservatory",
                      7: "Billiard room", 8: "Library", 9: "Study"}

        self.suspects = {1: "Miss. Scarlett", 2: "Colonel. Mustard", 3: "Mrs. White", 4: "Reverend. Green",
                         5: "Mrs. Peacock", 6: "Professor. Plum"}

        self.weapon = {1: "Knife", 2: "Candlestick", 3: "Revolver", 4: "Rope", 5: "Lead pipe", 6: "Wrench"}

        t1 = threading.Thread(target=self.listening)
        t1.start()

    # Eliminates Player's cards from possible choices.
    def initialise_cards(self, message):

        global initialised

        if not initialised:
            for i in message.split("'"):
                if i in self.possible_answer:
                    self.possible_answer.remove(i)
        initialised = True
        return None

    # Chooses a room from possible choices
    def choose_room(self):
        for key in self.rooms:
            if self.rooms[key] in self.possible_answer:
                self.send_message(str(key))
                break
        return None

    # Chooses suspect and weapon from possible choices.
    def choose_suspect_and_weapon(self):
        guess = ''
        for a in self.suspects:
            if self.suspects[a] in self.possible_answer:
                guess = str(a) + " "
                break
        for a in self.weapon:
            if self.weapon[a] in self.possible_answer:
                guess = guess + str(a)
                break
        self.send_message(guess)
        return None

    def send_message(self, bot_message):
        try:
            print(bot_message)
            self.user_socket.send(bot_message.encode("utf-8"))
        except Exception as error:
            print(f"Send Error:{error}")
        return None

    def bot_act_on_message(self, message):
        # Match incoming messages from game and react accordingly.
        global winning
        if 'Your Cards' in message and not initialised:
            self.initialise_cards(message)
        elif "Roll Dice" in message:
            time.sleep(1)
            self.send_message("y")
        elif 'Want to enter in a room' in message:
            time.sleep(1)
            choice = random.choices(['y', 'n'], weights=(98, 2))
            self.send_message(*choice)
        elif 'Choose a room to enter' in message:
            time.sleep(1)
            self.choose_room()
        elif 'Choose Suspect and Weapon' in message:
            time.sleep(1)
            self.choose_suspect_and_weapon()
        elif 'Do you want to revel cards' in message:
            time.sleep(1)
            if winning:
                choice = random.choices(['y', 'n'], weights=(98, 2))
            else:
                choice = random.choices(['y', 'n'], weights=(2, 98))
            self.send_message(*choice)
        elif re.fullmatch(pattern_1, message):
            self.possible_answer.remove(re.fullmatch(pattern_1, message).group(2))
        elif 'No proof against' in message:
            time.sleep(1)
            winning = True

    def listening(self):
        while True:
            try:
                message = self.user_socket.recv(1024).decode("utf-8")
                if not message:
                    break
                else:
                    print(message)
                    self.bot_act_on_message(message)
            except Exception as e:
                print(f"Error occurred: {e}")
                break
        return None


if __name__ == '__main__':
    ip_address = '127.0.0.1'
    print("Deploying Bot")
    Player(ip_address)
