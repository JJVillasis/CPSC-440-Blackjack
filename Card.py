class Card:

    #Constructor of Card object
    def __init__(self, value, face, suit):
        self.suit = suit
        self.face = face
        self.value = value

    #Instance of object when using repr()
    def __repr__(self):
        return str(self.face) + " of " + self.suit + "; Value = " + str(self.value)

    #Instance of object when using print()
    def __str__(self):
        return str(self.face) + " of " + self.suit
