# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 14:38:30 2020

@author: Nicholas Himes
"""


import numpy as np
import pandas as pd
import itertools

#%% Function
def assetPrices(pricesDF, h):
    N = 2517 #Size of the Stanford Dataset
    
    money = 1 #Start with $1
    
    r = [money] #Returns
    #Start of each day, invest h proportions of total money into the stocks
    
    for day in range(1, N):
        currentCol = 0 #Keep track of stock index so h can be called
        rDayTotals = []
        for stock in pricesDF:
            #pricesDF[stock] is the vector of prices
            
            Xd = pricesDF[stock][day] / pricesDF[stock][day-1]
            Rd = Xd * h[currentCol] * money
            rDayTotals.append(Rd) 
            currentCol += 1
        money = sum(rDayTotals) #Done going through all given stocks on that day, add it up to get new money amount
        r.append(money)
        
    return r

#%% Import Data
df = pd.read_csv("asset_prices.csv")

#%% Task 2 - Compute the optimal h for D = 2.
D = 2 #Select the first D stocks
hPossibilities = [i for i in itertools.product(np.linspace(0,1,21), repeat=D) if (sum(i)==1)]
rStorage = []
for h in hPossibilities:
    rDays = assetPrices(df.iloc[:,:D], h) #Give it the first two columns of stocks
    finalR = rDays[-1]
    rStorage.append(finalR)
    
maxMoney = max(rStorage)
maxIndex = rStorage.index(maxMoney)
winningPair = hPossibilities[maxIndex]
print("Optimal h at D={} was {} with ${}".format(D, winningPair, maxMoney))


#%% Task 3 - Compute the optimal h for D = 3.
D = 3 #Select the first D stocks
hPossibilities = [i for i in itertools.product(np.linspace(0,1,21), repeat=D) if (sum(i)==1)]
rStorage = []
for h in hPossibilities:
    rDays = assetPrices(df.iloc[:,:D], h) #Give it the first three columns of stocks
    finalR = rDays[-1]
    rStorage.append(finalR)
    
maxMoney = max(rStorage)
maxIndex = rStorage.index(maxMoney)
winningPair = hPossibilities[maxIndex]
print("Optimal h at D={} was {} with ${}".format(D, winningPair, maxMoney))
