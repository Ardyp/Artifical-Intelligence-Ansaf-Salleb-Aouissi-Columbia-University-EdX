# -*- coding: utf-8 -*-

import sys
import numpy as np
import csv 
from matplotlib import pyplot as plt
        
def pla(inputFile, inputX, inputLabel):
    #Initialize a zero weight matrix
    weight = np.zeros(inputX.shape[1])
    
    #Open csv file for writing
    file = open('output1.csv','w',newline='')
    writer = csv.writer(file)
    
    #Perform perceptron learning algorithm
    classificationError = 1
    while classificationError:
        classificationError = 0
        for x, label in zip(inputX, inputLabel):
            fxi = x.dot(weight)
            if fxi == 0:
                fxi = -1
            if label*fxi <= 0: #an error occurred
                weight = weight + label*x 
                classificationError = 1
        writer.writerow(weight)

    #Close csv file
    file.close()
    
    #Plot graph for visualization
    inputXpos1 = inputX[inputFile[:,2]==1,:]
    inputXneg1 = inputX[inputFile[:,2]==-1,:]
    plt.scatter(inputXpos1[:,0],inputXpos1[:,1], marker='+')
    plt.scatter(inputXneg1[:,0],inputXneg1[:,1], marker='o')
    plt.grid()
    #Plot decision boundary    
    x = np.linspace(min(inputX[:,0]),max(inputX[:,0]))
    y = (-weight[0]*x - weight[2])/weight[1]       
    plt.plot(x,y)
                 
def main():  
    #Read input file
    inputFile = np.genfromtxt(sys.argv[1], delimiter=',')
    #Form training data set
    inputTemp = inputFile[:,:-1]
    #Add a column of ones at the end for bias
    inputX = np.c_[inputTemp, np.ones(inputFile.shape[0])]
    #Form label set for training data               
    inputLabel = inputFile[:,-1:]
    #Check inputs created
#    print("---------")
#    print(inputFile)
#    print("---------")
#    print(inputX)
#    print("---------")
#    print(inputLabel)
#    print("---------")

    #Call perceptron learning algorithm
    pla(inputFile, inputX, inputLabel)
    
if __name__ == "__main__":
    main()
