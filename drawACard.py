"""
DRAW A CARD FUNCTION
input: playerNum -- an integer representing the index of the current player
       oldPos -- a pair of integers representing the player's position at the start of the turn
       newPos -- a pair of integers representing the player's position at the end of the turn
       PlayerList -- a list of player classes
       Primes -- a list of the prime numbers between 11 and 97
       Deck -- an ordered list of the cards still available to be drawn by a player
       DiscardPile -- a list of the cards that have been used/discarded

outputs: rollAgain -- a boolean telling the player whether they drew a "roll again" card
         PlayerList -- with possibly updated positions and hands
         Deck -- current deck after draw (and possible reshuffling)
         DiscardPile -- current discard pile after draw

Note: (1) Players only draw a (maximum of 1) card if one of their pawns ends on a prime
          that is distinct from where it started the turn.
      (2) This function makes use of the function bumpChecker

@author: David A. Nash
"""
import numpy as np
from bumpChecker import bumpChecker


def drawACard(playerNum,oldPos,newPos,PlayerList,Primes,Deck,DiscardPile):
    rollAgain = 0 ##a flag to denote whether the player drew a "Roll Again" event card
    posChangeFlag = 0 ##a flag to denote whether any players changed position as a result of a drawn card
    
    ##initialize a flag to determine which pawns (if any) landed on a new prime
    ##so 0 means 1st pos only, 1 means 2nd pos only, 2 means both are new
    newPrimeFlag = -1
    if newPos[0] in Primes and newPos[0] not in oldPos:
        newPrimeFlag += 1
    if newPos[1] in Primes and newPos[1] not in oldPos:
            newPrimeFlag += 2
            
    ##If both pawns land on a new prime then action cards can be applied to either
    ##So we need to choose which one
    ##for now, let's do that randomly
    if newPrimeFlag==2: 
        newPrimeFlag = np.random.randint(0,2) ##now newPrimeFlag denotes the pawn chosen
        
    ##If at least one pawn lands on a new prime, draw a card##
    if newPrimeFlag>-1:
        Draw = Deck[-1] ##draw the card off the "top" (back) of the deck
        Deck = Deck[:-1] ##remove the card drawn from the deck
        
        ##cards above 13 are the action cards which must be used immediately
        if Draw>13:
            DiscardPile.append(Draw) ##add the drawn card to the discard pile
            if Draw<17:  ##roll Again
                rollAgain = 1 
            elif Draw==17: ##50/50 type 1
                posChangeFlag = 1
                ##if the chosen pawn is below 50, add 50
                ##if it is above 50, subtract 50
                if newPos[newPrimeFlag] < 50: 
                    newPos[newPrimeFlag] += 50
                else:
                    newPos[newPrimeFlag] -= 50
            elif Draw==18: ##50/50 type 2
                posChangeFlag = 1
                ##if the chosen pawn is below 50, double it
                ##if it is above 50, subtract 10
                if newPos[newPrimeFlag] < 50:
                    newPos[newPrimeFlag] = newPos[newPrimeFlag]*2
                else:
                    newPos[newPrimeFlag] -= 10
            elif 18<Draw<21: ##advance/reverse to nearest
                ##get the current player pawn positions in order
                currLocs = []  
                for i in range(len(PlayerList)):
                    currLocs.append(PlayerList[i].position[0])
                    if PlayerList[i].position[1] != 101: #ignore pawns that have already left the board
                        currLocs.append(PlayerList[i].position[1])
                currLocs.sort()
                ##locate chosen pawn in the list
                idx = currLocs.index(newPos[newPrimeFlag])  
                if idx!=len(currLocs)-1 and Draw==19:  ##move forward if possible to nearest pawn and (later) bump it back to start
                    newPos[newPrimeFlag] = currLocs[idx+1]
                    posChangeFlag = 1
                elif idx!=0 and Draw==20:  ##move backward if possible to nearest pawn and (later) bump it back to start
                    newPos[newPrimeFlag] = currLocs[idx-1]
                    posChangeFlag = 1
            elif Draw == 21:  ##reverse digits
                digits = str(newPos[newPrimeFlag]) ##there are always exactly two digits on (eligible) Primes
                if digits[0] != digits[1]: ##don't do anything if the digits are the same
                    digits = digits[1]+digits[0]
                    newPos[newPrimeFlag] = int(digits)
                    posChangeFlag = 1
            elif Draw == 22:  ##Swap any two pawns
                if len(PlayerList)>1:  ##If there's only one player, swapping pawns is meaningless
                    ##choose two *distinct* players
                    swaps = np.array([0,0])
                    while swaps[0]==swaps[1]:  
                        swaps = np.random.randint(0,len(PlayerList),size=2)
                    ##choose a pawn for the first player
                    p1 = np.random.randint(0,2)  
                    if p1 == 1 and PlayerList[swaps[0]].position[1]==101: ##cannot swap with a pawn at 101
                        p1 = 0
                    ##choose a pawn for the second player
                    p2 = np.random.randint(0,2)  
                    if p2 == 1 and PlayerList[swaps[1]].position[1] == 101:
                        p2 = 0
                    ##Swap the two pawns
                    temp = PlayerList[swaps[0]].position[p1]
                    PlayerList[swaps[0]].position[p1] = PlayerList[swaps[1]].position[p2]
                    PlayerList[swaps[1]].position[p2] = temp
                    PlayerList[swaps[0]].position.sort()
                    PlayerList[swaps[1]].position.sort()
                    ##no need for change flag, since changes have been made and this cannot result in bumping
            elif Draw == 23:  ##Send to 64
                newPos[newPrimeFlag] = 64
                posChangeFlag = 1
            elif Draw == 24:  ##Steal a card
                ##First find the players who have cards
                stealable = []
                for i in range(len(PlayerList)):
                    if i != playerNum and len(PlayerList[i].cards)>0:
                        stealable.append(i)
                ##If at least one other player has cards, choose one randomly 
                ##and then choose a random card from their hand
                if len(stealable)>0:  
                    stealable = np.random.permutation(stealable)
                    stealfrom = stealable[0]
                    stealcard = PlayerList[stealfrom].cards[np.random.randint(0,len(PlayerList[stealfrom].cards))]
                    PlayerList[playerNum].cards.append(stealcard)
                    PlayerList[stealfrom].cards.remove(stealcard)
        else:  ##keep cards must be added to the hand, and cannot be used this turn
            PlayerList[playerNum].cards.append(Draw)
        ##Shuffle the discard pile to form a new deck when it is empty
        if len(Deck)<1:
            print("RESHUFFLING THE DISCARD PILE")
            Deck = np.random.permutation(DiscardPile)
            DiscardPile = [] 
    if posChangeFlag == 1:  ##an action card changed the players position, so recheck for bumping
        if newPos[0]==newPos[1]:  ##take care of self-bumping first
            newPos[0] = 0
            PlayerList[playerNum].position = newPos
        else:
            PlayerList[playerNum].position.sort
            bumpChecker(playerNum, PlayerList)
    return rollAgain, PlayerList, Deck, DiscardPile
