import Card
import random

class Deck:

    #Constructor of Deck object
    def __init__(self):
        self.cards = []
        self.build()

    #Append new deck of playing cards to current cards
    def build(self):
        #Classify the suits and values of the deck
        suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        faces = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

        #Append the cards to the current deck (+52)
        for suit in suits:
            for x in range(0,13):
                self.cards.append(Card.Card(values[x], faces[x], suit))

    #Print Technical information of each card in the deck
    def reprPrint(self):
        for card in self.cards:
            print(repr(card))

    #Print the cards in the deck
    def print(self):
        for card in self.cards:
            print(card)

    #Shuffle the order of the cards in the deck
    def shuffle(self):
        for x in range(len(self.cards) - 1, 0, -1):
            rIn = random.randint(0,x)
            self.cards[x], self.cards[rIn] = self.cards[rIn], self.cards[x]

    #Draw the top card from the deck
    def drawCard(self):
        return self.cards.pop()
