from Card import Card
import random
import pygame
import os

class Deck:

    #Constructor of Deck object
    def __init__(self):
        self.cards = []
        self.build()

    #Append new deck of playing cards to current cards
    def build(self):
        #Card graphic dimensions
        width = 200
        height = 300

        #Classify the suits and values of the deck
        suits = ["Spades", "Diamonds", "Clubs", "Hearts"]
        values = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        faces = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        folderPath = "Playing Cards"

        #Append the cards to the current deck (+52)
        for suit in range(4):
            for x in range(13):
                path = "S" + str(suit+1) + "-C" + str(x+1) + ".png"
                tempCard = pygame.image.load(os.path.join(folderPath, path))
                tempCard = pygame.transform.scale(tempCard, (width, height))
                self.cards.append(Card(values[x], faces[x], suits[suit], tempCard))

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
