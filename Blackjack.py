from Deck import Deck
from Player import Player
import time as t
from gpiozero import Button, LED
import random
import pygame

#Initialize pygame
pygame.init()

#Window dimensions
DISPLAY_WIDTH = 1800
DISPLAY_HEIGHT = 700

#Card graphic dimensions
CARD_WIDTH = 200
CARD_HEIGHT = 300

#Activate window
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("CPSC 440 - Blackjack")

#Card back graphic
folderPath = "Playing Cards"
path = "back.png"
cardBack = pygame.image.load(os.path.join(folderPath, path))
cardBack = pygame.transform.scale(cardBack, (CARD_WIDTH, CARD_HEIGHT))

#Game Font
myFont = pygame.font.SysFont("consolas", 75, ())

class Blackjack:

    #Constructor of object Blackjack
    def __init__(self, playerName):

        #Create the dealer, player, and deck objects
        self.dealer = Player("Dealer")
        self.player = Player(playerName)
        self.playingDeck = Deck()

        self.stand = False
        self.bust = False
        self.start = True
        
        #User input
        self.button = Button(14)    #Hit/Play again
        self.button2 = Button(15)   #Stand/Quit
        ##LED for global use
        self.ledG = LED(21)
        self.ledR = LED(20)
        self.ledB = LED(16)
        
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

    ########## Graphics Functions ##########

    #Lays the cards out one-by-one
    def cardFlourish(self):
        flourish = Deck()
        flourish.build()
        flourish.build()

        for x in range(len(flourish.cards)):
            num = x % 18
            gameDisplay.blit(flourish.cards[x].image, ((CARD_WIDTH * (num % 9)),(CARD_HEIGHT * int(num / 9))))
            pygame.display.update()
            sleep(.2)


    def drawStart(self):
        #Draw player Hand
        gameDisplay.blit(self.player.hand[0].image, (0, DISPLAY_HEIGHT - CARD_HEIGHT))
        pygame.display.update()
        sleep(.3)

        #Draw dealer Hand
        gameDisplay.blit(cardBack, (0, 0))
        pygame.display.update()
        sleep(.3)
        
        #Draw player Hand
        gameDisplay.blit(self.player.hand[1].image, (CARD_WIDTH + 5, DISPLAY_HEIGHT - CARD_HEIGHT))
        pygame.display.update()
        sleep(.3)

        #Draw dealer Hand
        gameDisplay.blit(self.dealer.hand[1].image, ((CARD_WIDTH + 5), 0))
        pygame.display.update()

        #Draw player Card Value
        playerVal = myFont.render("Player = " + str(self.player.cardValue()), 1, (0,0,0))
        gameDisplay.blit(playerVal, ((CARD_WIDTH * 2) + 10, DISPLAY_HEIGHT - CARD_HEIGHT))
        dealerVal = myFont.render("Dealer = ?" , 1, (0,0,0))
        gameDisplay.blit(dealerVal, ((CARD_WIDTH * 2) + 10, 0))
        pygame.display.update()

    def drawHands(self):
        gameDisplay.fill((0,150,0))
        pygame.display.update()

        #Draw starting hand
        if self.start:
            self.drawStart()
            self.start = False
            return

        #Draw player hand
        for x in range(len(self.player.hand)):
            gameDisplay.blit(self.player.hand[x].image, ((CARD_WIDTH * x) + (5 * x), DISPLAY_HEIGHT - CARD_HEIGHT))
        #Draw player card value
        playerVal = myFont.render("Player = " + str(self.player.cardValue()), 1, (0,0,0))
        gameDisplay.blit(playerVal, ((CARD_WIDTH * len(self.player.hand)) + (5 * len(self.player.hand)), DISPLAY_HEIGHT - CARD_HEIGHT))
        pygame.display.update()

        #Draw dealer hand
        if not stand and not bust:
            gameDisplay.blit(cardBack, (0, 0))

            for x in range(1, len(self.dealer.hand)):
                gameDisplay.blit(self.dealer.hand[x].image, ((CARD_WIDTH * x) + (5 * x), 0))
            #Draw player card value
            dealerVal = myFont.render("Dealer = ?" , 1, (0,0,0))
            gameDisplay.blit(dealerVal, ((CARD_WIDTH * len(self.dealer.hand)) + (5 * len(self.dealer.hand)), 0))
            pygame.display.update()

        else:
            for x in range(len(self.dealer.hand)):
                gameDisplay.blit(self.dealer.hand[x].image, ((CARD_WIDTH * x) + (5 * x), 0))
            dealerVal = myFont.render("Dealer = " + str(self.dealer.cardValue()), 1, (0,0,0))
            gameDisplay.blit(dealerVal, ((CARD_WIDTH * len(self.dealer.hand)) + (5 * len(self.dealer.hand)), 0))
            pygame.display.update()

    ########## Gameplay Functions ##########

    def gameplay(self):
        
        
        #Clear hands from previous game
        self.player.hand.clear()
        self.dealer.hand.clear()

        #Reset Start, Stand and Bust booleans
        self.bust = False
        self.stand = False
        self.start = True

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
            self.start = False

            self.showHand()
            self.drawHands()
            self.ledR.blink(on_time = .3 ,off_time = .1)
            print("21! Dealer Wins!")
            print()
            t.sleep(5)
            return


        ########## Player Turn ##########

        while self.stand == False and self.bust == False:

            #Show hands (Dealer hidden)
            self.showHand()
            self.drawHands()

            #Check if player hand == 21
            if(self.player.cardValue() == 21):
                self.stand = True
                self.ledG.blink(on_time = .1 ,off_time = .1)
                print("Winner!")
                print()
                t.sleep(5)
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
            self.ledB.blink()
            while True:
                if self.button.is_pressed:
                    self.ledB.off()
                    print("Player Input: Hit")
                    print()
                    option = "h"
                    t.sleep(.5)
                    break
                
                if self.button2.is_pressed:
                    self.ledB.off()
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
                    self.drawHands()
                    self.ledG.blink(on_time = .1 ,off_time = .1)
                    print("21! " + self.player.name + " Wins!")
                    print()
                    t.sleep(5)
                    return



                #Check if player hand is over 21
                elif self.player.cardValue() > 21:
                    #Check if aceChange lowers hand <= 21
                    if(self.aceChange(self.player) == False):
                        #Else bust
                        self.bust = True

                        #Show hands (Dealer visible)
                        self.showHand()
                        self.drawHands()
                        self.ledR.blink(on_time = .3 ,off_time = .1)
                        print(self.player.name + " bust!")
                        print()
                        t.sleep(5)
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
        self.drawHands()
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
                    self.drawHands()
                    self.ledG.blink(on_time = .1 ,off_time = .1)
                    print("Dealer bust!")
                    print()
                    t.sleep(5)
                    return

            self.showHand()
            self.drawHands()
            t.sleep(1)

        ########## Hand Comparisons ###########

        #Player wins
        if self.player.cardValue() > self.dealer.cardValue():
            self.ledG.blink(on_time = .1 ,off_time = .1)
            print(self.player.name + " Wins!")
            print()
            t.sleep(5)

        #Dealer wins
        elif self.dealer.cardValue() > self.player.cardValue():
            self.ledR.blink(on_time = .3 ,off_time = .1)
            print(self.player.name + " Loses.")
            print()
            t.sleep(5)


        else:
            self.ledB.on()
            print(self.player.name + " Breaks Even.")
            print()
            t.sleep(5)



    def play(self):
        quit = False

        while not quit:
            self.gameplay()
                
            print("Do you wish to play again?")
            print()
            self.ledG.blink(on_time = .5)
            self.ledR.blink(on_time = .4)
            self.ledB.blink(on_time = .3)
            
            #Button input
            while True:
                    if self.button.is_pressed:
                        print("Player Input: Play Again")
                        print()
                        Quit = False
                        t.sleep(.5)
                        self.ledG.off()
                        self.ledR.off()
                        self.ledB.off()
                        break
                    
                    if self.button2.is_pressed:
                        print("Player Input: Quit")
                        print()
                        quit = True
                        t.sleep(.5)
                        self.ledG.off()
                        self.ledR.off()
                        self.ledB.off()
                        break