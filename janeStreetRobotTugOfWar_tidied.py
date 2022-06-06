# -*- coding: utf-8 -*-
"""
Created on Mon May 30 21:00:14 2022

@author: Y-dee

# README: Jane Street Puzzle 
"""

import random
import pandas as pd
import seaborn as sns
import time
    
def playGame(start, interval, cutOff, stepSize):
    
    flag = start
    rounds = 0
    cutOffReached = False
    
    p2Win = -0.5*interval
    p1Win = 0.5*interval
    
    randDistance = 0
    # stepSize = 1 as default. https://www.w3schools.com/python/ref_random_randrange.asp#:~:text=Python%20Random%20randrange%20%28%29%20Method%201%20Definition%20and,position%20to%20end.%20An%20integer%20specifying%20the%20incrementation.
    
    while rounds <= cutOff:
        
        if flag >= p1Win:
            #print("P1 win")
            return 1
        elif flag <= p2Win:
            #print("P2 win")
            return 2
        
        # P1 moves
        randDistance = (random.randrange(0,interval, stepSize))
        if rounds%2 == 0:  #is even then p1 move
            #p1 moves        
            #print("p1 moves to the right: ", randDistance)
            flag += randDistance 
        else:
            #randDistance = (random.randrange(-interval,0, stepSize))
            flag -= randDistance
            #print("p2 moves to the left: ", randDistance)
        
        #print("flag is", flag)
        
    
        rounds += 1
    
    return -1 # no return
    
def playMultipleGames(numIterations, interval, cutOff, stepSize):
    
    result = [[0,0]]
    p1ResultsMatrix = []
    
    gamesPlayed = 0
    
    #interval = 100
    #cutOff = 100
    #stepSize = 1
    
    start = -interval//2
    finish = interval//2
    
    current = start
    
    
    while current < finish:
        
        p1Wins = 0
        p2Wins = 0
        
        for i in range(0, numIterations):        
            
            winner = playGame(current, interval, cutOff, stepSize)
            
            if winner == 1:
                p1Wins +=1
            if winner == 2:
                p2Wins += 1
                # terminated before winner
            #print("i is ", i)  
        #print(p1Wins, " p1 wins")
        #print(p2Wins," p2 wins")
        p1Pct, p2Pct = computePercentages(p1Wins, p2Wins)
        
        p1ResultsMatrix.append([current, p1Pct])
        
        current += 1
    return p1ResultsMatrix


def computePercentages(p1Wins, p2Wins):
    
    p1Pct = p1Wins/(p1Wins + p2Wins)
    p2Pct = 1 - p1Pct
    return p1Pct, p2Pct
        
def convertResultsToDataFrame(resultsMatrix):
    #https://datatofish.com/column-as-index-pandas-dataframe/
    df = pd.DataFrame(resultsMatrix, columns = ["position", "p1WinPct"]) 
    #df.set_index("position")
    
    return df

def graphResults(df):
    sns.lineplot(data = df, x = "position", y = "p1WinPct")
    return

def deNoiseResults(df):
    # smoothing signal using averaging
    
    windows = [10,100,1000]
    rollingAvgSignalList = []
    
    for windowSize in windows:
        rollingAvgSignalList.append(df.rolling(windowSize,None, True).mean())
    
    return rollingAvgSignalList

def computeClosestToFairGameIndex(avgSignalList):
    
    indexList = []
    for df in avgSignalList:
        closestToFairGame = pd.Series(abs(df.iloc[:,1]-0.5))
        index = closestToFairGame.argmin()
        indexList.append(index)
        
    return indexList

def getLocationOfFairGame(indexList, avgSignalList):
    
    locationList = []
    
    for index, df2 in zip(indexList, avgSignalList):
    # https://stackoverflow.com/questions/40846137/iterate-through-2-lists-at-once-in-python
            location = df2.iloc[index,0]
            locationList.append(location)
    return locationList

if __name__ == "__main__":
    
    # rough runtimes
    # interval 1e4, iteration 1e2: ~5s 
    # interval 1e4, iteration 1e3: ~42s
    # interval 1e5, iteration 1e3: ~420-530s (~7-9 mins)
    # interval 1e6, iteration 2e3: ~10,000s (~2hrs 40mins)
    
    start = time.perf_counter()
    runtimeDf = []
    interval = 1e6
    cutOff = 1e3
    stepSize = 1
    
    numIterations = int(2e3)
    
    p1Results = playMultipleGames(numIterations, interval, cutOff, stepSize)
    
    df = convertResultsToDataFrame(p1Results)
    graphResults(df)
    
    rollingAvgSignalList = deNoiseResults(df)
    indexList = computeClosestToFairGameIndex(rollingAvgSignalList)
    finalLocations = getLocationOfFairGame(indexList, rollingAvgSignalList)
    
    
    finish = time.perf_counter()
    runtime = round(finish - start,2)
    print(f'Finished in {runtime} seconds')
    
    runtimeDf.append([interval, numIterations, runtime])
    print(finalLocations)