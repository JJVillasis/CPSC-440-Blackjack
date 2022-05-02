from Deck import Deck
from Player import Player
import time as t
from gpiozero import Button
import random

class Blackjack:

    #Constructor of object Blackjack
    def __init__(self, playerName):

        #Create the dealer, player, and deck objects
        self.dealer = Player("Dealer")
        self.player = Player(playerName)
        self.playingDeck = Deck()

        self.stand = False
        self.bust = False
        
        #User input
        self.button = Button(14)    #Hit/Play again
        self.button2 = Button(18)   #Stand/Quit

        #Play the game with a 3-deck shoe (Append 2 decks to playing deck)
        self.playingDeck.build()
        self.playingDeck.build()

        #shuffle the shoe 5-10 times
        shuffle = random.randint(5, 10)
        for x in range(0, shuffle):
            self.playingDeck.shuffle()

    #Change ace value from 11 to 1
    def aceChange(self, player):
        change = False

        for x in player.hand:
            if x.face == "Ace" and x.value == 11:
                x.value = 1
                change = True

        return change

    #Print hand and card value of the player
    def showHand(self):

        print("==============================\n")

        #Print Player hand
        print(self.player.name + "\'s Hand = " + str(self.player.cardValue()))
        self.player.printHand()
        print()

        #Dealer hand
        if (self.stand == False and self.bust == False):
            #Limited hand visibility
            print("Dealer\'s Hand = " + "?")
            print("X")
            print(self.dealer.hand[1])
            print()

        else:
            print("Dealer\'s Hand = " + str(self.dealer.cardValue()))
            self.dealer.printHand()
            print()

        print("==============================\n")

    #Print Options that are currently available to the player
    def playerOptions(self):
        print("Available Options:")

        #Always available to the player
        print("H = Hit")
        print("S = Stand")
        print()

    def gameplay(self):
        #Clear hands from previous game
        self.player.hand.clear()
        self.dealer.hand.clear()

        #Deal cards to the player and dealer
        self.player.draw(self.playingDeck)
        self.dealer.draw(self.playingDeck)
        self.player.draw(self.playingDeck)
        self.dealer.draw(self.playingDeck)

        #self.player.hand.append(c.Card(11, "Ace", "Spades"))
        #self.player.hand.append(c.Card(11, "Ace", "Clubs"))

        #Check if dealer has 21
        if self.dealer.cardValue() == 21:
            self.bust = True

            self.showHand()

            print("21! Dealer Wins!")
            print()
            return


        ########## Player Turn ##########

        while self.stand == False and self.bust == False:

            #Show hands (Dealer hidden)
            self.showHand()

            #Check if player hand == 21
            if(self.player.cardValue() == 21):
                self.stand = True
                print("Winner!")
                print()
                return

            #Check if player got >21 (double aces)
            elif self.player.cardValue() > 21:
                self.aceChange(self.player)

            #Show Player options
            self.playerOptions()

            #Player input
            #option = input("Player: ")
            #print()
            
            #Button input
            option = ""
            
            while True:
                if self.button.is_pressed:
                    print("Player Input: Hit")
                    print()
                    option = "h"
                    t.sleep(.5)
                    break
                
                if self.button2.is_pressed:
                    print("Player Input: Stand")
                    print()
                    option = "s"
                    t.sleep(.5)
                    break
            
            

            #Hit - Add card to player hand
            if option.lower() == "h":
                self.player.draw(self.playingDeck)

                #If player gets 21
                if self.player.cardValue() == 21:
                    self.stand = True

                    #Show hands (Dealer visible)
                    self.showHand()

                    print("21! " + self.player.name + " Wins!")
                    print()
                    return



                #Check if player hand is over 21
                elif self.player.cardValue() > 21:
                    #Check if aceChange lowers hand <= 21
                    if(self.aceChange(self.player) == False):
                        #Else bust
                        self.bust = True

                        #Show hands (Dealer visible)
                        self.showHand()

                        print(self.player.name + " bust!")
                        print()
                        return

            #stand
            elif option.lower() == "s":
                self.stand = True

            #Unknown Command
            else:
                print("Unknown Command. Please Try again.")
                print()

        ########## Dealer Hand ###########

        print("========== Dealer's Turn ==========")
        print()

        #Show hand (Dealer visible)
        self.showHand()
        t.sleep(1)

        #If dealer card value < 16, hit until >= 16
        while self.dealer.cardValue() < 16:
            self.dealer.draw(self.playingDeck)

            #If dealer card value > 21
            if self.dealer.cardValue() > 21:
                #Check if aceChange lowers hand <= 21
                if(self.aceChange(self.dealer) == False):

                    #Dealer Bust

                    #Show hands (Dealer visible)
                    self.showHand()

                    print("Dealer bust!")
                    print()
                    return

            self.showHand()
            t.sleep(1)

        ########## Hand Comparisons ###########

        #Player wins
        if self.player.cardValue() > self.dealer.cardValue():
            print(self.player.name + " Wins!")
            print()

        #Dealer wins
        elif self.dealer.cardValue() > self.player.cardValue():
            print(self.player.name + " Loses.")
            print()

        else:
            print(self.player.name + " Breaks Even.")
            print()


    def play(self):
        quit = False

        while not quit:
            self.gameplay()

            print("Do you wish to play again?")
            print()

            #Button input
            while True:
                    if self.button.is_pressed:
                        print("Player Input: Play Again")
                        print()
                        Quit = False
                        t.sleep(.5)
                        break
                    
                    if self.button2.is_pressed:
                        print("Player Input: Quit")
                        print()
                        quit = True
                        t.sleep(.5)
                        break