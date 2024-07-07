# le-her

[german readme](README.md)

## requirements

Required Programs :
- Python 3 (https://www.python.org/)

Required Python Modules :
- numpy (https://numpy.org/)
    >> pip install numpy
- pyqt5 (https://pypi.org/project/PyQt5/)
    >> pip install PyQt5
    
## game rules

The game is a 2 player game (here one player is replaced by the game ai).  
1 player plays as the dealer and the other plays as the player.  
A round of le her starts with the player drawing a card from the deck, followed by the dealer drawing a card from the deck.  
Then the player has the option to swap cards with the dealer.  
If the dealer has a king, the swap fails (both cards are revealed in either case).  
Then the dealer has the option to draw a new card from the deck and place the old card on top of the deck.  
If the next card on the deck is a king, the redraw fails (in either case the player is not shown any of the cards).  
Then the round is over and the next round starts.  
A game of le her lasts for 13 rounds.  
After that every player sums up the values of their cards (Ace = 1p, 2 = 2p, ... ,10 = 10p, Jack = 11p, Queen = 12p, King = 13p).  
The player with the higher score wins.  
