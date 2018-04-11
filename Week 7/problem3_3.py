# -*- coding: utf-8 -*-

import sys
import numpy as np
import csv 
from collections import namedtuple
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

def algorithms(kernelChoice):
    global splitset
    
    #Assign parameter space 
    if kernelChoice == 'linear':
        parameters = {'kernel': ('linear',), 'C': [0.1, 0.5, 1, 5, 10, 50, 100]}
        estimator = svm.SVC()
        subPlotNum = 1
    elif kernelChoice == 'poly':
        parameters = {'kernel': ('poly',), 'C': [0.1, 1, 3], 'degree': [4, 5, 6], 'gamma': [0.1, 0.5]}
        estimator = svm.SVC()
        subPlotNum = 2
    elif kernelChoice == 'rbf':
        parameters = {'kernel': ('rbf',), 'C': [0.1, 0.5, 1, 5, 10, 50, 100], 'gamma': [0.1, 0.5, 1, 3, 6, 10]}
        estimator = svm.SVC()
        subPlotNum = 3
    elif kernelChoice == 'logisticregression':
        parameters = {'C': [0.1, 0.5, 1, 5, 10, 50, 100]}
        estimator = LogisticRegression()
        subPlotNum = 4
    elif kernelChoice == 'knn':
        parameters = {'n_neighbors': range(1, 51), 'leaf_size': range(5, 61, 5)}
        estimator = KNeighborsClassifier()
        subPlotNum = 5
    elif kernelChoice == 'decisiontrees':
        parameters = {'max_depth': range(1, 51), 'min_samples_split': range(2, 11)}
        estimator = DecisionTreeClassifier()
        subPlotNum = 6
    elif kernelChoice == 'randomforest':
        parameters = {'max_depth': range(1, 51), 'min_samples_split': range(2, 11)}
        estimator = RandomForestClassifier()
        subPlotNum = 7    
    
    #Searching for the best parameters in the model
    clf = GridSearchCV(estimator, parameters, cv=5, n_jobs=10)
    clf.fit(splitset.X_train, splitset.y_train)
    # The chosen model
    print(kernelChoice, clf.best_estimator_)
    classifier = clf.best_estimator_
    #Score of best_estimator on the left out data
    trainScoreBest = clf.best_score_
    #Score obtained using the test set
    testScore = classifier.score(splitset.X_test, splitset.y_test)
    #Plot prediction boundary on test data
    meshPlot(kernelChoice,classifier,subPlotNum)
    
    return trainScoreBest, testScore 

def scatterPlot(data):
    #Initialize figure and plot initial data
    fig1 = plt.figure(1)
    #For plotting scaled data
    ax1 = fig1.add_subplot(111)
    posSample = data[:,2] == 1
    negSample = data[:,2] == 0
    ax1.scatter(data[posSample,0], data[posSample,1], marker='+', c='blue')
    ax1.scatter(data[negSample,0], data[negSample,1], marker='o', c='red')
    ax1.set_xlabel('A')
    ax1.set_ylabel('B')
    ax1.set_title('Scatter plot')

def meshPlot(kernelChoice,classifier,subPlotNum):
    global fig2
    global splitset
    
    #For plotting scaled data
    ax = fig2.add_subplot(2,4,subPlotNum)
    # create a mesh to plot in
    h = 0.2  # step size in the mesh
    x1_min, x1_max = splitset.X_test[:, 0].min() - 1, splitset.X_test[:, 0].max() + 1
    x2_min, x2_max = splitset.X_test[:, 1].min() - 1, splitset.X_test[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, h), np.arange(x2_min, x2_max, h))

#    classifier.fit(splitset.X_train, splitset.y_train)
    Z = classifier.predict(np.c_[xx1.ravel(), xx2.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx1.shape)
    ax.contourf(xx1, xx2, Z, cmap=plt.cm.coolwarm, alpha=0.8)
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_title(kernelChoice)
    
    # Plot also the test point actual labels
    ax.scatter(splitset.X_test[:, 0], splitset.X_test[:, 1], c=splitset.y_test, cmap=plt.cm.coolwarm)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())
    
    
def main():  
    #Close all open figures
    plt.close("all")
    
    #Read input file
    with open(sys.argv[1]) as inp, open('tmpInput3.csv', 'w') as out:
        txt = inp.read()
        txt = txt.replace('\r', '\n')
        out.write(txt)
    data = np.genfromtxt('tmpInput3.csv', delimiter=",",skip_header=1) #skip header while reading

    #Visualize data
#    scatterPlot(data)
    
    #Extract input data and corresponding labels
    X = data[:,:-1] #data input
    y = data[:,-1] #labels    

    #Define namedtuple for split set of data
    dataset = namedtuple('dataset', 'X_train X_test y_train y_test')
    # Stratified split test-train data
    output = train_test_split(X, y, test_size=0.4, random_state=42, stratify = y)
    global splitset
    splitset = dataset._make(output)

    #Open csv file for writing
    fHandle = open('output3.csv','w',newline='')
    writer = csv.writer(fHandle)    

    #Initialize figure and plot initial data
    global fig2
    fig2 = plt.figure(2)
    
    #Call various learning algorithm
    trainScoreBest, testScore = algorithms('linear')
    writer.writerow(['svm_linear', trainScoreBest, testScore])  
    trainScoreBest, testScore = algorithms('poly')
    writer.writerow(['svm_polynomial', trainScoreBest, testScore])
    trainScoreBest, testScore = algorithms('rbf')
    writer.writerow(['svm_rbf', trainScoreBest, testScore])
    
    trainScoreBest, testScore = algorithms('logisticregression')
    writer.writerow(['logistic', trainScoreBest, testScore])
    trainScoreBest, testScore = algorithms('knn')
    writer.writerow(['knn', trainScoreBest, testScore])
    trainScoreBest, testScore = algorithms('decisiontrees')
    writer.writerow(['decision_tree', trainScoreBest, testScore])
    trainScoreBest, testScore = algorithms('randomforest')
    writer.writerow(['random_forest', trainScoreBest, testScore])

    #Close CSV file
    fHandle.close()
    
if __name__ == "__main__":
    main()
