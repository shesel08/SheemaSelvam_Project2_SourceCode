# SheemaSelvam_Project2_SourceCode

## Clue/Cluedo: The Classic Mystery Game
The object of the game is to determine who murdered the game's victim, where the crime took place, and which weapon was used.
Each player assumes the role of one of the six suspects and attempts to deduce the correct answer by strategically moving around a game board representing the rooms of a mansion and collecting clues about the circumstances of the murder from the other players.
The game consists of a board which shows the rooms, corridors, and secret passages of an English country house called Tudor Mansion/Boddy Mansion.
The game box also includes several coloured playing pieces to represent characters, miniature murder weapon props, two six-sided dice, three sets of cards (describing the aforementioned rooms, characters, or weapons), Solution Cards and an envelope (or a mirror in some editions) to contain one card from each set of cards and a Detective's Notes pad on which are printed lists of rooms, weapons, and characters, so players can keep detailed notes during the game.
The murder victim in the game was known as Mr. Boddy in North American versions.

The six suspects are:
* Miss. Scarlett
* Colonel. Mustard
* Mrs. White
* Reverend. Green
* Mrs. Peacock
* Professor. Plum

The weapons are:
* Candlestick
* Knife
* Lead pipe
* Revolver
* Rope
* Wrench

There are nine rooms in the mansion where the murder could have taken place. 
* Hall
* Lounge
* Dining room
* Kitchen
* Ballroom
* Conservatory
* Billiard room
* Library
* Study

The project can be cloned from GitHub using the url - https://github.com/shesel08/SheemaSelvam_Project2_SourceCode.git

To execute the game, execute 
Server/Bot execution - python Main.py
Client - python Client.py by respective players

The user experience has been enhanced to allow just bots or the users can interact over TCP host ip address to play the game. The user can also control how many bots/players can play this game. The least required players are 3 and max is 6. 
The user can choose the server type which has options as 
1. With player bots offline 
2. Offline Server 
2. Online Server

In the first option, the players involved are bots, and they make random decisions based on the weightage provided for each decision. 
With the second option, the players can connect over same local ip address and play the game.
With the third option, the players can play over internet using Google DNS to get the IP address.
In case of both second and third option, each player should have Client.py in their local and edit the ip address in that file to connect to the game server. 
The game server is up after selecting the option for server_type. Once the server is up, the players can connect to it by running the Client.py with updated ip address and continue playing the game.

The murder solution with suspect, weapon and room are separated first and removed from the deck. The remaining cards are shuffled and distributed between the players. 
The players can make suggestion or accusation. But if the accusation is incorrect, the same player can not make accusation again.
The game ends when all players are removed from making accusation or one player wins.


