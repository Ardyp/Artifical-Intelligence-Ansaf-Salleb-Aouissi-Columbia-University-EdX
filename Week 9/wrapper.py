# -*- coding: utf-8 -*-

import driver_3
import sys

def main(filenameSudokuStart,filenameSudokuFinish): 
    #This function iterates the driver_3.py file through each sudoku puzzle
    failedIndex = []
    with open(filenameSudokuStart,'r') as sudokuStart, open(filenameSudokuFinish,'r') as sudokuFinish:
        for index, (sudokuStartStr, sudokuFinishStr) in enumerate(zip(sudokuStart, sudokuFinish)):
            if index in [0]: #For error checking of specific test cases
                driver_3.main(sudokuStartStr) #Run the main sudoku solver file
                with open('output.txt','r') as sudokuTest:
                    sudokuTestStr = sudokuTest.readline()
                sudokuFinishStr = sudokuFinishStr.rstrip('\r\n') #Remove the newline character at the end
                if sudokuTestStr != sudokuFinishStr:
                    failedIndex.append(index)
                print('TestCase = ',index,', Passed?:', bool(sudokuTestStr == sudokuFinishStr))

    #Check whether all testcases passed
    print('All passed?: ', not len(failedIndex)) 
    print('Failed indices: ',failedIndex)       
    
if __name__ == "__main__":
    filenameSudokuStart = sys.argv[1]
    filenameSudokuFinish = sys.argv[2]
    main(filenameSudokuStart,filenameSudokuFinish)
    