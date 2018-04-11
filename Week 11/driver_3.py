# -*- coding: utf-8 -*-

import os
import pandas as pd
import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier

def imdb_data_preprocess(inpath, name):
    '''Implement this module to extract
    and combine text files under train_path directory into 
    imdb_tr.csv. Each text file in train_path should be stored 
    as a row in imdb_tr.csv. And imdb_tr.csv should have two 
    columns, "text" and label'''

    folderList = ['pos/','neg/']    
    outputFile = open(name,'w',encoding='utf-8',newline='')
    writer = csv.writer(outputFile)
    writer.writerow(['','text','polarity'])
    index = -1
    for folder in folderList:
        inpathCurrent = inpath + folder  
        for root, dirs, filenames in os.walk(inpathCurrent):
            for filename in filenames:
                index = index + 1
                token1 = filename.split('_')
                rating = token1[1].split('.')
                with open(inpathCurrent + filename,'r',encoding="utf-8") as inputfile:
                    text = inputfile.read()
                processedText = processText(text)
                writer.writerow([index,processedText,int(int(rating[0])>5)]) 
    outputFile.close()

def processText(text):
    global stopWordSet
    #Replace unwanted characters with spaces
    replacedText = text.replace('<br />', ' ')
    #Remove all punctuation marks
    chars = ".,?!;:-_/<>~`@#$%^&*()+=[]{}|\\\"\'"
    for c in chars:
        replacedText = replacedText.replace(c,' ')    
    #Convert string into a list of words
    replacedTextList = replacedText.split()
    #Remove stopwords from the list of words
    processedText = ' '.join([word for word in replacedTextList if word.lower() not in stopWordSet])
    
    return processedText
        
def train_tdm(trainData, ngram, tfidf):
    global stopWordList
    if tfidf:
        vectorizer = TfidfVectorizer(ngram_range = (1,ngram), stop_words = stopWordList)
    else:
        vectorizer = CountVectorizer(ngram_range = (1,ngram), stop_words = stopWordList)        
    termDocMatrix =  vectorizer.fit_transform(trainData['text'])
    vocabulary = vectorizer.vocabulary_
    clf = SGDClassifier(loss='hinge', penalty='l1')
    clf.fit(termDocMatrix, trainData['polarity'])
    
    return vocabulary, clf   
    
def test_tdm(testData, ngram, vocabulary, clf, tfidf):     
    global stopWordList
    if tfidf:
        vectorizer = TfidfVectorizer(ngram_range = (1,ngram), stop_words = stopWordList, vocabulary = vocabulary)
    else:            
        vectorizer = CountVectorizer(ngram_range = (1,ngram), stop_words = stopWordList, vocabulary = vocabulary)       
    termDocMatrix = vectorizer.fit_transform(testData['text'])
    resultList = clf.predict(termDocMatrix)
    
    return resultList    
    
def write2file(filename,resultList):
    with open(filename,'w',newline='') as outputFile:
        writer = csv.writer(outputFile)
        for result in resultList:
            writer.writerow([result]) 

def main():  
    global stopWordSet
    global stopWordList

    #Vocareum platform path    
    train_path = "../resource/lib/publicdata/aclImdb/train/" # use terminal to ls files under this directory
    test_path = "../resource/lib/publicdata/imdb_te.csv" # test data for grade evaluation
    #Local drive path
#    train_path = "aclImdb/train/" # use terminal to ls files under this directory
#    test_path = "imdb_te.csv" # test data for grade evaluation
    #Test local drive path
#    train_path = "aclImdb/train/" # use terminal to ls files under this directory
#    test_path = "imdb_te_TRY.csv" # test data for grade evaluation   
    #Location to store mixed training data
    train_path_combined = "imdb_tr.csv"
    
    #Load the stopwords and put them into a set
    with open("stopwords.en.txt",'r') as inputfile:
        stopWordList = inputfile.read().splitlines()
    stopWordSet = set(stopWordList)
    
    #Combine the positive and negative examples from train set
    imdb_data_preprocess(inpath = train_path, name = train_path_combined)     
    #Read in the combined train data
    trainData = pd.read_csv(train_path_combined, encoding="utf-8") #train data has header
    #Read in the test data
    testData = pd.read_csv(test_path, encoding = "ISO-8859-1") #test data has header
    #Clean up the test data by applying processText to it
    testData['text'] = testData['text'].apply(processText)
    #Sanity check
#    print(testData.head())
#    print(trainData.head())   

    #---------------------------------#
    #Predict using Unigram
    vocabulary, clf = train_tdm(trainData,ngram = 1,tfidf=False)
    resultList = test_tdm(testData,ngram = 1,vocabulary = vocabulary,clf=clf,tfidf=False) 
    #Print results
    write2file("unigram.output.txt",resultList)    
    #---------------------------------#    
    #Predict using Bigram approach
    vocabulary, clf = train_tdm(trainData,ngram = 2,tfidf=False)
    resultList = test_tdm(testData,ngram = 2,vocabulary=vocabulary,clf=clf,tfidf=False) 
    #Print results
    write2file("bigram.output.txt",resultList)  
    #---------------------------------#    
    #Predict using Unigram with tfidf
    vocabulary, clf = train_tdm(trainData,ngram = 1,tfidf=True)
    resultList = test_tdm(testData,ngram = 1,vocabulary=vocabulary,clf=clf,tfidf=True) 
    #Print results
    write2file("unigramtfidf.output.txt",resultList)  
    #---------------------------------#    
    #Predict using Bigram with tfidf
    vocabulary, clf = train_tdm(trainData,ngram = 2,tfidf=True)
    resultList = test_tdm(testData,ngram = 2,vocabulary=vocabulary,clf=clf,tfidf=True) 
    #Print results
    write2file("bigramtfidf.output.txt",resultList)  
    #---------------------------------#       
    
if __name__ == "__main__":
    main()
