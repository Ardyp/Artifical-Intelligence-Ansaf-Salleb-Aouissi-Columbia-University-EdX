# -*- coding: utf-8 -*-

import sys
import copy
import itertools
import queue
    
def createSudokuCsp():
    global sudokuConstraint
    
    #Create domain values
    domain = [1,2,3,4,5,6,7,8,9]
    #Create sudoku board containing all the variables
    sudokuBoard = [['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9'],
                   ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9'],
                   ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                   ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9'],
                   ['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9'],
                   ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9'],
                   ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'],
                   ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9'],
                   ['I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9']]
    #Assign domain values for each variable
    sudokuDomain = {key:list(domain) for row in sudokuBoard for key in row}
    #Create a copy of sudoku dictionary to store value assignment for each variable   
    sudokuAssign = {key:0 for key in sudokuDomain}

    #Create constraints
    constraintList = []
    #Constraints along row
    for row in sudokuBoard:       
        constraintList = constraintList + list(itertools.permutations(row,2))
    #Constraints along column
    sudokuBoardT = list(map(list,zip(*sudokuBoard))) #Transpose the sudoku board 
    for col in sudokuBoardT:       
        constraintList = constraintList + list(itertools.permutations(col,2))
    #Constraints within each 3x3 square
    for row in [0,3,6]:
        for col in [0,3,6]:
            box = [val for row in sudokuBoard[row:row+3] for val in row[col:col+3]]    
            constraintList = constraintList + list(itertools.permutations(box,2))
    #Remove duplicate constraints
    constraintList = list(set(constraintList))
    #Create a dictionary to store constraints. Initialize constraints to empty lists.
    sudokuConstraint = {key:list([]) for key in sudokuDomain} 
    #Associate the constraints with their respective keys in a dictionary
    for val in constraintList:
        sudokuConstraint[val[0]].append(val) 
        
    return sudokuAssign, sudokuDomain, constraintList

def selectUnassignedVariable(sudokuAssign,sudokuDomain):
    #Minimum remaining values heuristic is used
    MRV = 100 #A randomly chosen number larger than domain size
    for row in 'ABCDEFGHI':
        for col in '123456789':
            if sudokuAssign[row+col] == 0: #Consider only unassigned variables
                value = sudokuDomain[row+col]
                if len(value) < MRV:
                    MRV = len(value)
                    chosenKey = row+col 
    return chosenKey 

def consistent(sudokuAssign, sudokuDomain, chosenKey, value):
    global sudokuConstraint
    
    constraintList = sudokuConstraint[chosenKey]
    for constraint in constraintList:
        if value == sudokuAssign[constraint[1]]:
            return False 
    return True

def inference(sudokuAssign, sudokuDomain, chosenKey, value):
    #This inference function implements forward checking

    global sudokuConstraint
    
    constraintList = sudokuConstraint[chosenKey]
    for constraint in constraintList:
        checkKey = constraint[1]
        if sudokuAssign[checkKey] == 0: #Perform forward checking only on unassigned variables
            if value in sudokuDomain[checkKey]:
                sudokuDomain[checkKey].remove(value)
            if not sudokuDomain[checkKey]: #If domain is empty, i.e., no legal values remaining 
                return (False, sudokuAssign, sudokuDomain)
    return (True, sudokuAssign, sudokuDomain)
    
def backtracksearch(sudokuAssign,sudokuDomain):  
    #Check if assignment is complete
    if all(value>0 for key,value in sudokuAssign.items()):
        return (True, sudokuAssign, sudokuDomain)
    chosenKey = selectUnassignedVariable(sudokuAssign,sudokuDomain)
    for value in sudokuDomain[chosenKey]:
        if consistent(sudokuAssign, sudokuDomain, chosenKey, value):
            sudokuAssignNew = copy.deepcopy(sudokuAssign)
            sudokuDomainNew = copy.deepcopy(sudokuDomain)
            sudokuAssignNew[chosenKey] = value
            sudokuDomainNew[chosenKey] = [value]
            resultInference = inference(sudokuAssignNew, sudokuDomainNew, chosenKey, value)
            if resultInference[0] == True:
                resultBTS = backtracksearch(resultInference[1],resultInference[2])
                if resultBTS[0] == True:
                    return resultBTS
    return (False, sudokuAssign, sudokuDomain)

def makeAssign(sudokuAssign, sudokuDomain):
    for key,value in sudokuDomain.items():
        if len(value) == 1:
            sudokuAssign[key] = value[0]
    return sudokuAssign    

def getNeighbours(Xi):
    global sudokuConstraint
    neighbours = [Xk for Xi, Xk in sudokuConstraint[Xi]]
    return neighbours
    
def revise(sudokuDomain, Xi, Xj):
    revised = False
    for x in sudokuDomain[Xi]:
        if not any(y!=x for y in sudokuDomain[Xj]):
            sudokuDomain[Xi].remove(x)
            revised = True
    return revised

def AC3(sudokuAssign,sudokuDomain, constraintList):  
    q = queue.Queue()
    for constraint in constraintList:
        q.put(constraint)
    while not q.empty():
        Xi,Xj = q.get()
        if revise(sudokuDomain, Xi, Xj):
            if not sudokuDomain[Xi]:
                return (False, sudokuAssign, sudokuDomain)
            for Xk in getNeighbours(Xi):
                q.put((Xk,Xi))
    sudokuAssign = makeAssign(sudokuAssign, sudokuDomain)
    return (True, sudokuAssign, sudokuDomain)

def visualizeBoard(sudokuAssign):
    #Prints a sudoku grid containing the assigned variables.
    #This function accepts a dictionary of the form:
    #sudokuAssign = {'A1':1, 'A2':4, 'A3':8, 'A4':0, 'A5':0, 'A6':7, 'A7':5, 'A8':0, 'A9':3,
    #                'B1':3, 'B2':0, 'B3':2, 'B4':0, 'B5':4, 'B6':0, 'B7':9, 'B8':0, 'B9':1,
    #                   :
    #                   :
    #                'I1':2, 'I2':8, 'I3':4, 'I4':0, 'I5':6, 'I6':0, 'I7':0, 'I8':3, 'I9':9,}
    #'0' values indicate unassigned variables and will not be printed.                         

    s = ""
    line = "-------------------------------------\n"
    s += line
    for row in "ABCDEFGHI":
        s += "|"
        for col in "123456789":
            if sudokuAssign[row + col] != 0:
                s += ("%3d" % sudokuAssign[row + col]) + "|"
            else:
                s += ("%3c" % ' ') + "|"
        s += "\n" + line
    
    print(s)
           
def main(sudokuStrStart):
    #Initialize sudoku assignments, domain, and constraints
    sudokuAssign, sudokuDomain, constraintList = createSudokuCsp()
    
    #Load sudoku starting board
    index = -1
    for j in 'ABCDEFGHI':
        for i in '123456789':
            key = j+i
            index = index + 1
            sudokuAssign[key] = int(sudokuStrStart[index])
            if int(sudokuStrStart[index]) != 0:
                sudokuDomain[key] = [int(sudokuStrStart[index])]

    print('Starting sudoku board')
    visualizeBoard(sudokuAssign)

    #Run AC3 algorithm first.             
    flag, sudokuAssignNew, sudokuDomainNew = AC3(copy.deepcopy(sudokuAssign),copy.deepcopy(sudokuDomain), copy.deepcopy(constraintList))
    algoName = 'AC3'
    #If the assignment is consistent after AC3, copy the assigned values into respective variables 
    if flag == True:
        sudokuAssign = sudokuAssignNew
        sudokuDomain = sudokuDomainNew
    if all(value>0 for key,value in sudokuAssignNew.items()):
        pass #All variables have been successfully assigned by AC3 algorithm 
    else: #If AC3 fails, use the reduced domain space and BTS to solve the puzzle
        print('Mid sudoku board')
        visualizeBoard(sudokuAssign) 
        flag, sudokuAssign, sudokuDomain = backtracksearch(copy.deepcopy(sudokuAssign),copy.deepcopy(sudokuDomain))
        algoName = 'BTS'
    
    print('Completed sudoku board')
    visualizeBoard(sudokuAssign) 
    
    #Create the sudoku string from the sudoku assignment dictionary
    sudokuStrFinish = ''
    index = -1
    for j in 'ABCDEFGHI':
        for i in '123456789':
            key = j+i
            sudokuStrFinish = sudokuStrFinish + str(sudokuAssign[key])

    #Write output to file
    file = open("output.txt","w")
    file.write('{} {}'.format(sudokuStrFinish,algoName))
    file.close()
    
if __name__ == "__main__":
    #Input sudoku string
    sudokuStrStart = sys.argv[1]
#    sudokuStrStart = '000000000302540000050301070000000004409006005023054790000000050700810000080060009'
    #Call main function
    main(sudokuStrStart)
