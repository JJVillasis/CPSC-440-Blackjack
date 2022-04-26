import Deck

class Player:

    #Constructor of hand object
    def __init__(self, name):
        self.name = name
        self.hand = []

    #Instance of object when using repr()
    def __repr__(self):
        return "Player: " + self.name + "; Cards in Hand = " + str(len(self.hand))

    #Instance of object when using print()
    def __str__(self):
        return self.name

    #Draw a card from the deck and add it to the hand
    def draw(self, deck):
        self.hand.append(deck.drawCard())
        return self

    #Return sum of values of cards in hand    
    def cardValue(self):
        sum = 0
        for x in self.hand:
            sum += x.value

        return sum

    #Print cards found in hand
    def printHand(self):
        for card in self.hand:
            print(card)
