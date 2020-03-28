"""
TAKE TURN FUNCTION
input: playerNum -- index of current player
       PlayerList -- list of player classes
       Primes -- a list of the primes from 11 to 97
       Deck -- integer list of cards available to be drawn
       DiscardPile -- integer list of cards in the discard pile
       Spots -- a list of the possible positions on the board
       printData -- a boolean determining whether to print outcomes

output: an integer index of the player to take the next turn
        PlayerList -- updated with any changes from the turn
        Deck -- updated
        DiscardPile -- updated

Note: (1) Due to the rules of Prime Climb, no pawns can leave position 101.
      (2) This function requires cursePlayer, moveMapper, bumpChecker, sendPlayerHome, drawACard

@author: David A. Nash
"""
import numpy as np
from BasicGameData import Player
from bumpChecker import bumpChecker
from cursePlayer import cursePlayer
from drawACard import drawACard
from moveMapper import moveMapper
from sendPlayerHome import sendPlayerHome

def takeTurn(playerNum, PlayerList, Primes, Deck, DiscardPile, Spots, printData):
    ##at the start of the turn, randomly decide whether to curse another player (if the card is available)
    curseFlag = 0
    if 12 in PlayerList[playerNum].cards:
        curseFlag = np.random.randint(0,2) ##randomly choose whether to use the card or not
        card = 12
    elif 13 in PlayerList[playerNum].cards:
        curseFlag = np.random.randint(0,2)
        card = 13
    if curseFlag == 1:
        cursePlayer(card,playerNum,PlayerList,DiscardPile)
    
    ##Get the current player position, roll the dice, and generate the possible moves
    pos = PlayerList[playerNum].position
    roll = [np.random.randint(0,10),np.random.randint(0,10)]
    if printData == True:
        print('Player {} rolled:'.format(playerNum), roll)
    possibleMoves = moveMapper(roll,pos,PlayerList[playerNum].cards,PlayerList[playerNum].cursed, Spots)

    ##choose to win if you can
    if 101 in possibleMoves[:,0]:
        Move = np.array([101,101]).reshape((1,2))
        print("Player ", playerNum, " wins!!!!")
        return -1*(playerNum+1), PlayerList, Deck, DiscardPile
    ##if 101 is an option for pawn2, don't consider other options
    elif 101 in possibleMoves: 
        TryToWin = np.where(possibleMoves[:,1]==101)[0] ##find indices of moves with 101 as one of the positions
        possibleMoves = possibleMoves[TryToWin]
        ##choose a random move
        Move = possibleMoves[np.random.randint(0,possibleMoves.shape[0])]
    else:
        ##choose a random move
        Move = possibleMoves[np.random.randint(0,possibleMoves.shape[0])]
        
    ##ADD CHECK TO AVOID USING CARDS IF IT IS POSSIBLE TO GET TO THE CHOSEN LOCATION WITH FEWER OF THEM
    if Move.shape[0]>2 and Move[2] != 100000000000: 
        x = np.where(possibleMoves[:,0]==Move[0])[0]
        y = np.where(possibleMoves[:,1]==Move[1])[0]
        matches = np.intersect1d(x,y)  ##finds indices of all locations matching chosen Move
        ##first in the list should have the lowest third entry (saving lower number cards)
        bestMove = possibleMoves[matches[0],:]
        ##It may be possible to use fewer cards though, so check
        for j in range(len(matches)):
            if sum(int(digit) for digit in str(possibleMoves[j,2])[1:]) < sum(int(digit) for digit in str(bestMove[2])[1:]):
                bestMove = possibleMoves[j,:]
        Move = bestMove
        
        ##Check if any cards were used and discard them
        if Move[2] != 100000000000:  
            for i in range(1,len(str(Move[2]))):
                if str(Move[2])[i]=='1':
                    PlayerList[playerNum].cards.remove(i)
                    DiscardPile.append(i)
    
    ##Change the current player's position to the newly chosen one (drop the card encoding)
    PlayerList[playerNum].position = Move[0:2]
    if printData == True:
        print('Player {} moves to:'.format(playerNum), Move[0:2])
    
    ##Check for bumping, note: self bumping is already achieved in moveMapper
    bumpChecker(playerNum, PlayerList)
    
    ##undo any curses at the end of the turn
    if PlayerList[playerNum].cursed == True:
        PlayerList[playerNum].cursed = False
        if printData == True:
            print('Player {} is no longer cursed'.format(playerNum))
    
    ##if the player did not use the send home cards to augment their own move, they can choose to send someone else back
    if 10 in PlayerList[playerNum].cards:
        if np.random.randint(0,2)==1:
            sendPlayerHome(10,playerNum,PlayerList,DiscardPile)
    if 11 in PlayerList[playerNum].cards:
        if np.random.randint(0,2)==1:
            sendPlayerHome(11,playerNum,PlayerList,DiscardPile)
            
    ## after all actions, check to see if they get to draw a card 
    rollAgain, PlayerList, Deck, DiscardPile = drawACard(playerNum, pos, Move[0:2],PlayerList,Primes,Deck,DiscardPile)
    
    if rollAgain == True:  ##take another turn!
        return playerNum, PlayerList, Deck, DiscardPile
    else:  ##move to next player
        return (playerNum+1)%len(PlayerList), PlayerList, Deck, DiscardPile
