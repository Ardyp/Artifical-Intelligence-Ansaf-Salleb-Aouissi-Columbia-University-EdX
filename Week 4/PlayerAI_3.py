# -*- coding: utf-8 -*-

import time
import numpy as np
import itertools
from random import randint
from BaseAI_3 import BaseAI
from Grid_3 import Grid
from Displayer_3  import Displayer
from ComputerAI_3 import ComputerAI

actionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}

playerAllowance = 0.02
playerTimeLimit = 0.2 - playerAllowance # Time Limit before Losing
playerPrevTime = 0
playerAlarm = False
tileValues = [2, 4]
#tileValues = [2]
probability = 0.9
MAXDEPTH = 4
        
def playerUpdateAlarm():
    global playerTimeLimit
    global playerPrevTime
    global playerAlarm
    if (time.clock() - playerPrevTime) >= playerTimeLimit:
        playerAlarm = True
    else: 
        playerAlarm = False
    return playerAlarm
    
def terminalTest(grid):
    if grid.depth >= MAXDEPTH or (not grid.canMove()):
        return True
    else:
        return False

def absSub(x,y):
    return abs(x-y)        

def evaluateUtility(grid):    
    #Number of empty cells. Higher -> better
    totCell = len(grid.getAvailableCells())
    h1 = totCell/(grid.size*grid.size)

    #Smoothness of tiles. Lower -> better
    totDiff = 0
    #Along each column
    for i in range(grid.size - 1):
        totDiff += sum(list(map(absSub, grid.map[i], grid.map[i+1])))
    #Along each row 
    for i in range(grid.size):    
        totDiff += sum(list(map(absSub, grid.map[i][:-1], grid.map[i][1:])))

    totCell = sum(itertools.chain.from_iterable(grid.map))
    h2 = totDiff/(2*totCell) #Divided by 2 to ensure maximum normalised value is 1
    
#    for i in grid.map:
#        print(i)
#    print("h1= {:.4f}".format(h1))
#    print("h2= {:.4f}".format(h2))
#    print ("h1 - h2 = {:.4f}".format(h1-h2))
#    print(" ----> next option")

    return h1 - h2    
    
def minPlay(grid,alpha,beta):
    global playerTimeLimit
    global playerPrevTime
    global playerAlarm
    #Terminal node test
    if terminalTest(grid):
        return (None, evaluateUtility(grid))
        
    #Reset minChild and minUtility
    (_, minUtility) = (None, np.inf)
    
    #Check each child with empty cell filled iwth '2' or '4'
    cells = grid.getAvailableCells()
    
    for cellValue in tileValues:
        for cell in cells:
            childGrid = grid.clone()
            childGrid.depth = grid.depth + 1 #Increment the depth of node
            childGrid.insertTile(cell,cellValue)
            (_, utility) = maxPlay(childGrid, alpha, beta)
            
            if utility < minUtility:
                (minMove, minUtility) = (cell, utility)
                
            if minUtility <= alpha:
                break
            
            if minUtility < beta:
                beta = minUtility

            if playerAlarm or playerUpdateAlarm():
#                print("minPlay, Alarm={}, Time={:.6f}, Depth={}".format(playerAlarm,(time.clock() - playerPrevTime),grid.depth))
                break
            
        if playerAlarm or playerUpdateAlarm():
#            print("minPlay, Alarm={}, Time={:.6f}, Depth={}".format(playerAlarm,(time.clock() - playerPrevTime),grid.depth))
            break
                
    return (minMove, minUtility)
        
def maxPlay(grid,alpha,beta):
    global playerTimeLimit
    global playerPrevTime
    global playerAlarm
    #Terminal node test
    if terminalTest(grid):
        return (None, evaluateUtility(grid))

    #Reset maxChild and maxUtility
    (_, maxUtility) = (None, -np.inf)
    
    #Check each child in the [UP, DOWN, LEFT, RIGHT] = [0, 1, 2, 3] direction
    moves = grid.getAvailableMoves()
    
    for move in moves:
        childGrid = grid.clone()
        childGrid.depth = grid.depth + 1 #Increment the depth of node
        childGrid.move(move)
#        print("Option : {}".format(actionDic[move]))
        (_, utility) = minPlay(childGrid, alpha, beta)
        
        if utility > maxUtility:
            (maxMove, maxUtility) = (move, utility)
            
        if maxUtility >= beta:
#            print("maxutility={:.3f} and beta={:.3f} and depth={}".format(maxUtility,beta,grid.depth))
#            print("Pruned at {}".format(move))
            break
        
        if maxUtility > alpha:
            alpha = maxUtility
            
        if playerAlarm or playerUpdateAlarm():
#            print("maxPlay, Alarm={}, Time={:.6f}, Depth={}".format(playerAlarm,(time.clock() - playerPrevTime),grid.depth))
            break
          
#    print("Returned alpha={:.3f} and beta={:.3f} and depth={}".format(alpha,beta,grid.depth))    
    return (maxMove, maxUtility)
    
class PlayerAI(BaseAI):        
    def __init__(self):      
        pass
        
    def getMove(self, grid):
        global playerTimeLimit
        global playerPrevTime
        global playerAlarm
        playerAlarm = False
        playerPrevTime = time.clock() #Start timer
#        print("Start time {:.4f}".format(playerPrevTime))
        grid.depth = 0
        (child, _) = maxPlay(grid, -np.inf, np.inf)
#        print("Time lapsed {:.4f}".format(time.clock() - playerPrevTime))
        return child

'''        
def getNewTileValue():
    if randint(0,99) < 100 * probability:
        return tileValues[0]
    else:
        return tileValues[-1];        
        
if __name__ == '__main__':
    g = Grid()
#    g.map[0][0] = 2
#    g.map[1][0] = 2
#    g.map[3][0] = 4
    
    g.map =[[2,  0,  0,  0],
            [2,  0,  0,  0],
            [0,  0,  0,  0],
            [0,  0,  0,  0]]

    computer = ComputerAI()
    player = PlayerAI()
    displayer = Displayer()
    key = 'a'
    
    while key != 'q' and g.canMove():
        for i in g.map:
            print(i)
        print('-------')
        print(g.getAvailableMoves())
        print('-------')

        #Player turn    
        newMove = player.getMove(g)
        print("Current Move: " + actionDic[newMove])
        g.move(newMove)
        
        #Computer turn
        newMove = computer.getMove(g)
        g.setCellValue(newMove, getNewTileValue())

        #Wait for user verification
        print("User input to continue")
#        key = input()              
'''