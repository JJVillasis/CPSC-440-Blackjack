import Deck as d
import Player as p
import random

class Blackjack:

    #Constructor of object Blackjack
    def __init__(self, playerName):

        #Create the dealer, player, and deck objects
        self.dealer = p.Player("Dealer")
        self.player = p.Player(playerName)
        self.playingDeck = d.Deck()

        #Play the game with a 3-deck shoe (Append 2 decks to playing deck)
        self.playingDeck.build()
        self.playingDeck.build()

        #shuffle the shoe 5-10 times
        shuffle = random.randint(5, 10)
        for x in range(0, shuffle):
            self.playingDeck.shuffle()

    def play(self):

        #Deal cards to the player and dealer
        self.player.draw(self.playingDeck)
        self.dealer.draw(self.playingDeck)
        self.player.draw(self.playingDeck)
        self.dealer.draw(self.playingDeck)

    #Print Options that are currently available to the player
    def playerOptions(self):
        print("Available Options:")

        #Always available to the player
        print("H = Hit")
        print("S = Stand")
