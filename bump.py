"""
BUMP FUNCTION
Check for pawns that land on one another and bump back to start

input: board -- a (3n,1)-array where n is the number of players
                e.g. if n=2, [p1.pos1,p1.pos2,p2.pos1,p2.pos2,p1.turn,p2.turn]

output: fixedBoard -- (3n,1)-array of positions after bumping

Note: (1) Due to the rules of Prime Climb, no pawns can leave position 101.

@author: David A. Nash
"""
import numpy as np

##Check for overlapping pawns and bump back to start.
def bump(board):
    n = board.shape[0]//3 ##number of players
    order = board[-n:,0] ##array of one-hots for player turn
    idx = np.where(order==1)[0][0] ##current player
    fixedBoard = np.zeros(board.shape) ##initialize post-bump board
    fixedBoard[2*n+idx,0]=1 ##keep the current player
    playerList = set(np.arange(0,n)) - set([idx]) ##remove current player from set
    pos1 = board[2*idx:2*idx+2,0] ##position for current player
    fixedBoard[2*idx:2*idx+2,0] = pos1
    for player in playerList:
        temp = [0,0] ##initialize temp position for other player
        pos2 = board[2*player:2*player+2,0]
        if pos2[0] not in pos1 or pos2[0]==101: temp[0]=pos2[0]
        if pos2[1] not in pos1 or pos2[1]==101: temp[1]=pos2[1]
        temp.sort() ##sort to ensure they are in increasing order
        fixedBoard[2*player:2*player+2,0] = temp
    
    return fixedBoard.astype(int)