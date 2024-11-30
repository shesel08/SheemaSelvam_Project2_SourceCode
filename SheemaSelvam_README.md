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

This game is coded for player agents to make moves and make selections in the same computer with an IP specified to act as a game server.
The Player.py adds a player with every run. Hence, if you want to play the game with 3 players, then execute Player.py 3 times in 3 different terminals.
This gives a feel like 3 different players are playing the game, and it shows the cards and choices of that player in the terminal. 
The name of the player is picked randomly to identify each of them uniquely. 
Cluedo.py has the main code for the game which starts execution once all players have joined the game.
The communication between the players and the game server is maintained over messages.

To execute the game, follow the below steps in order.

* python Cluedo.py

* python Player.py


