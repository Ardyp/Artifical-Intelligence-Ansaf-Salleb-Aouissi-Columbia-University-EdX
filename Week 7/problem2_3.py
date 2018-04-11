# -*- coding: utf-8 -*-

import sys
import numpy as np
import csv 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
   
def linearRegression(inputFile, inputX, inputLabel, mean, std):
    #Initialize the learning rates
    alphaList = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 0.98]
    iterationMaxList = [100, 100, 100, 100, 100, 100, 100, 100, 100, 58]

    #Number of training data samples
    n = inputX.shape[0]
    #Open csv file for writing
    fileHandle = open('output2.csv','w',newline='')
    writer = csv.writer(fileHandle)

    #Initialize figure and plot initial data
    fig1 = plt.figure(1)
    #For plotting scaled data
    ax1 = fig1.add_subplot(121, projection='3d')
    plotX1scaled = np.arange(inputX[:,1].min(), inputX[:,1].max(), 0.2)
    plotX2scaled = np.arange(inputX[:,2].min(), inputX[:,2].max(), 0.2)
    plotX1scaled, plotX2scaled = np.meshgrid(plotX1scaled, plotX2scaled)
    ax1.set_xlabel('age(years)')
    ax1.set_ylabel('weight(kilograms)')
    ax1.set_zlabel('height(meters)')
    ax1.scatter(inputX[:,1], inputX[:,2], inputLabel)
    ax1.set_title('Scaled inputs')
    #For plotting unscaled data
    ax2 = fig1.add_subplot(122, projection='3d')
    plotX1unscaled = np.arange(inputFile[:,0].min(), inputFile[:,0].max(), 0.2)
    plotX2unscaled = np.arange(inputFile[:,1].min(), inputFile[:,1].max(), 0.2)
    plotX1unscaled, plotX2unscaled = np.meshgrid(plotX1unscaled, plotX2unscaled)
    ax2.set_xlabel('age(years)')
    ax2.set_ylabel('weight(kilograms)')
    ax2.set_zlabel('height(meters)')
    ax2.scatter(inputFile[:,0], inputFile[:,1], inputLabel)
    ax2.set_title('Unscaled inputs')
    #For plotting learning curve
    fig2 = plt.figure(2)
    ax3 = fig2.add_subplot(111)
    ax3.set_title('Learning Curve')
    
    #Start gradient descent
    for alpha, iterationMax in zip(alphaList,iterationMaxList):
        #Initialize the risk to empty list
        risk = []
#        storeMinRisk = float('inf')
        #Initialize a zero weight matrix
        weight = np.zeros(inputX.shape[1])
        for iterationNum in range(iterationMax):
            #Compute the predicted output for all input training data 
            fx = inputX.dot(weight)
            #Compute risk function
            risk.append((1/(2*n))*sum((fx-inputLabel.flatten())**2))
            #Update weight vector
            temp1 = (fx[:,None]-inputLabel).flatten()
            temp2 = (inputX*temp1[:,None]).sum(axis=0)
            weight = weight - (alpha/n)*temp2
            
#            #Find optimum alpha and iteration length
#            if iterationNum >= 1 and risk[-1]<storeMinRisk:
#                storeMinRisk = risk[-1]
#                iterationMin = iterationNum + 1
#            if iterationNum == 0:
#                storeMinRisk = risk[0]
#                iterationMin = iterationNum + 1
#            if iterationNum >= 1 and risk[-1]>risk[-2]:
#                break
#        print("alpha:",alpha,", iteration:",iterationMin,", minRisk: ",storeMinRisk)    
                
        #Write weight vector to csv file for current alpha value
        val = np.hstack(([alpha,iterationMax], weight))
        writer.writerow(val)
    
        #Plot learning curve for current alpha value
        ax3.plot(range(len(risk)),risk)
        #PLot boundary surface for scaled data
        plotZ = (weight[0] + weight[1]*plotX1scaled + weight[2]*plotX2scaled)
        ax1.plot_surface(plotX1scaled, plotX2scaled, plotZ)
        #Plot boundary surface for unscaled data
        weightUnscaled = unscaledWeight(weight, mean, std) 
        plotZunscaled = (weightUnscaled[0] + weightUnscaled[1]*plotX1unscaled + weightUnscaled[2]*plotX2unscaled)
        ax2.plot_surface(plotX1unscaled, plotX2unscaled, plotZunscaled)
    
    #Close csv file
    fileHandle.close()     

def unscaledWeight(weightScaled, mean, std):
    weightUnscaled = np.zeros(weightScaled.shape)
    temp1 = mean/std
    weightUnscaled[0] = weightScaled[0] - weightScaled[1:].dot(temp1)
    weightUnscaled[1:] = weightScaled[1:]/std
    return weightUnscaled

def normalizeData(data):
    mean = data.mean(axis=0)
    std = data.std(axis=0)
    data = data - mean[None,:]
    data = data/std[None,:]                 
    return data, mean, std
    
def main():  
    #Read input file
    inputFile = np.genfromtxt(sys.argv[1], delimiter=',')
    #Form training data set
    inputTemp = inputFile[:,:-1]
    #Normalize data
    inputTemp, mean, std = normalizeData(inputTemp)
    #Add a column of ones at the start for bias
    inputX = np.c_[np.ones(inputFile.shape[0]), inputTemp]
    #Form label set for training data               
    inputLabel = inputFile[:,-1:]
#    #Check inputs created
#    print("---------")
#    print(inputFile)
#    print("---------")
#    print(inputX)
#    print("---------")
#    print(inputLabel)
#    print("---------")

    #Call linear regression learning algorithm
    linearRegression(inputFile, inputX, inputLabel, mean, std)
    
if __name__ == "__main__":
    main()
