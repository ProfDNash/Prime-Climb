"""
CLEAN POSITIONS FUNCTION
    input: iP1 -- a list of potential positions (obtained from applying dice/cards)
           Spots -- a list of all positions on the board, typically [0,1,...,101]

This function eliminates any positions which are not allowed (e.g. non-integer, or off the board)
and also deletes any duplicates

@author: David A. Nash
"""
import numpy as np

def cleanPositions(iP1, Spots=np.arange(102)):
    ##make sure each position is listed in increasing order
    iP1=np.sort(iP1)
    
    ##then sort different positions into increasing order (lex)
    if iP1.shape[1]>2:  ##when considering cards, we have the encoding value too
        iP1.view('float,float,float').sort(order=['f0','f1'], axis=0)  
    else:
        iP1.view('float,float').sort(order=['f0'], axis=0)
        
    deleteRows=np.array([]) ##keep track of things to delete
    compareRow=None ##current row we're comparing to (for repeats)
    for idx, pos in enumerate(iP1):
        if (pos[0] not in Spots) or (pos[1] not in Spots):
            ##mark row for deletion if off the board
            deleteRows = np.append(deleteRows, idx) 
        elif np.array_equal(pos, compareRow):
            ##mark duplicates for deletion
            deleteRows = np.append(deleteRows, idx) 
        else:
            compareRow=pos  ##reassign currentRow if we run into a new allowable position
    deleteRows = deleteRows.astype(int)
    iP1 = np.delete(iP1, deleteRows, axis=0)
    return iP1
