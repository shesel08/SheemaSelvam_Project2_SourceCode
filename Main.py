import time
import sys
import socket

from GameBot import GameBot
from Server import CluedoGameServer


if __name__ == '__main__':
    # Card categories
    SUSPECTS = ["Miss. Scarlett", "Colonel. Mustard", "Mrs. White", "Reverend. Green", "Mrs. Peacock",
                "Professor. Plum"]
    WEAPONS = ["Knife", "Candlestick", "Revolver", "Rope", "Lead pipe", "Wrench"]
    ROOMS = ["Hall", "Lounge", "Dining room", "Kitchen", "Ballroom", "Conservatory", "Billiard room", "Library",
             "Study"]

    player_names = ["Alice", "Bob", "Charlie", 'Peter', 'Jane', 'Rose']

    n_players = int(input("Enter the number of players (3-6)\n(Least 3 players are recommended)\n"))
    if type(n_players) == int and 6 >= n_players >= 3:
        possible_names = []
        for i in range(n_players):
            possible_names.append(player_names[i])
    else:
        print("Invalid character entered.")
        sys.exit(1)

    print("________________Setting up the Game Server__________________")
    server_type = input("Choose the type of server...\n1. With player bots offline \n2. Offline Server"
                        "\n3. Online Server\n")

    if server_type == '1':
        game = GameBot(possible_names, SUSPECTS, WEAPONS, ROOMS)

        win = False
        while not win and len(game.playersWhoCanMakeAccusation) != 0:
            game.show_player_deck_and_points()
            time.sleep(1)
            win = game.player_turn()
            print("\n\n")

        if len(game.playersWhoCanMakeAccusation) == 0:
            print("All players have been removed from making accusations")
        print("Thanks for playing.")

    elif server_type == "2":
        ipaddress = "127.0.0.1"  # Local host IP address.
        cluedo = CluedoGameServer(ipaddress, possible_names, n_players, SUSPECTS, WEAPONS, ROOMS)
        cluedo.accept_requests()

    elif server_type == "3":
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server.connect(
                ("8.8.8.8", 80))  # Using Google DNS -To get your IPV4 Address.
            server_type = server.getsockname()[0]
            print(f"Players can connect using: {server_type} address.")
            server.close()
        except Exception as online_error:
            print(f"{online_error}: Check your internet connection.")
            sys.exit(1)
    else:
        print("Invalid option !")
        sys.exit(1)
