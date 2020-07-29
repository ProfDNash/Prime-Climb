"""
TRAINING FUNCTION
Run through multiple games using the Learn Game function, to train NN

input: parameters -- a dictionary containing parameters for each layer of the network, 'W1', 'b1', etc.
       lambd -- parameter controlling the network's *memory* (lambd==1 perfect memory)
       alpha -- learning rate parameter
       numGames -- the number of games to play through
       eps -- parameter controlling the amount of random exploration allowed in training

output: winners -- an array counting of the number of wins for each player
        turns -- an list containing the number of turns for each game
        params -- updated parameters based on learning from one game


@author: David A. Nash
"""
import numpy as np
from learnGame import learnGame

def train(parameters, lambd=0, alpha=0.01, numGames=10, eps=0.99):
    ##initialize counters
    winners = np.array([0,0])
    turns = list()
    params=parameters.copy()
    for g in range(numGames):
        if g%2==0: print('Game:',g)
        Xlist, Ylist, turn, params, winner = learnGame(params, lambd, alpha, eps)
        turns.append(turn)
        winners[winner] += 1
        eps *= 0.99
        
    return winners, turns, params