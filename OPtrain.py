"""
ONE PLAYER TRAINING FUNCTION
Run through multiple games using the Learn Game function, to train NN

input: parameters -- a dictionary containing parameters for each layer of the network, 'W1', 'b1', etc.
       lambd -- parameter controlling the network's *memory* (lambd==1 perfect memory)
       alpha -- learning rate parameter
       numGames -- the number of games to play through
       eps -- parameter controlling the amount of random exploration allowed in training
       learn -- a boolean parameter controlling whether the network learns as it plays

output: turns -- an list containing the number of turns for each game
        params -- updated parameters based on learning from one game


@author: David A. Nash
"""

import pickle
from onePlayer import onePlayerGame


def OPtrain(parameters, lambd=0, alpha=0.01, numGames=10, eps=0.99, learn=True):
    ##initialize counters
    turns = list()
    params = parameters.copy()
    for g in range(numGames):
        if g % 10 == 0:
            print("Game:", g)
        Xlist, Ylist, turn, params = onePlayerGame(params, lambd, alpha, eps, learn)
        turns.append(turn)
        if learn == True:
            eps *= 0.999
            if g % 100 == 0:
                f = open("params3.pkl", "wb")
                pickle.dump(params, f)
                f.close()
                g = open("turns3.pkl", "wb")
                pickle.dump(turns, g)
                g.close()

    return turns, params
