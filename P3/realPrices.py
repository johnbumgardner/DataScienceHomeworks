# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 14:38:30 2020

@author: Nicholas Himes
"""


import numpy as np
import pandas as pd
import itertools
import matplotlib.pyplot as plt

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

def indices(a, func):
    return [i for (i, val) in enumerate(a) if func(val)]

def linsearch(data, D):
    #data = grid for visualizing signal
    f=data-np.log(data) # signal values

    plt.figure(figsize=(8, 8))
    plt.title("Linear Search, D={}".format(D))
    plt.plot(data,f)

    #-------
    # optimize
    #-------
    xmax=np.max(data)
    xmin=np.min(data)

    for iter in range(1,11):
        grid_here=np.arange(xmin,xmax,(xmax-xmin)/10)
        fhere=3*grid_here-np.log(grid_here) # compute function
        location_min = indices(fhere, lambda n: n == np.min(fhere))# index where f is minimal 
        min_loc = location_min[0]+1
        next_min = np.max((min_loc-2,1)) # compute indices for next iteration
        next_max=np.min((min_loc+2,len(grid_here)))
        xmin=grid_here[next_min-1] # actual edges for next iteration
        xmax=grid_here[next_max-1]
        print ('xmin='+str((xmin+xmax)/2) + ', fmin=' +str(fhere[location_min][0]) + ', interval width=' +str(xmax-xmin) + '\n')
        

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

plt.figure(1)
plt.plot(np.linspace(0,1,21), rStorage)
plt.xlabel('First h index')
plt.ylabel('R')
plt.title("D=2")


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

#Can't plot this because four variables is too many dimensions
#r = f(a,b,c)

plt.figure(2)
plt.plot(df.iloc[:,0])
plt.xlabel("Day")
plt.ylabel("Stock Price")
plt.title("Stock 0: American Express")

plt.figure(3)
plt.plot(df.iloc[:,2])
plt.xlabel("Day")
plt.ylabel("Stock Price")  
plt.title("Stock 2: BP")


D = 4 #Select the first D stocks
hPossibilities = [i for i in itertools.product(np.linspace(0,1,21), repeat=D) if (sum(i)==1)]
rStorage = []
for h in hPossibilities:
    rDays = assetPrices(df.iloc[:,:D], h) #Give it the first three columns of stocks
    finalR = rDays[-1]
    rStorage.append(finalR)
maxIndex = rStorage.index(maxMoney)
winningPair = hPossibilities[maxIndex]
print("Optimal h at D={} was {} with ${}".format(D, winningPair, maxMoney))    

#%% Linear Search

D = 2 #Select the first D stocks
hPossibilities = [i for i in itertools.product(np.linspace(0,1,21), repeat=D) if (sum(i)==1)]
rStorage = []
for h in hPossibilities:
    rDays = assetPrices(df.iloc[:,:D], h) #Give it the first two columns of stocks
    finalR = rDays[-1]
    rStorage.append(finalR)

maxMoney = max(rStorage)
maxIndex = rStorage.index(maxMoney)
linsearch(rStorage, D)
convexMaxIndex = np.argmax(rStorage - np.log(rStorage))
print(maxIndex, convexMaxIndex)

D = 3 #Select the first D stocks
hPossibilities = [i for i in itertools.product(np.linspace(0,1,21), repeat=D) if (sum(i)==1)]
rStorage = []
for h in hPossibilities:
    rDays = assetPrices(df.iloc[:,:D], h) #Give it the first three columns of stocks
    finalR = rDays[-1]
    rStorage.append(finalR)
    
maxMoney = max(rStorage)
maxIndex = rStorage.index(maxMoney) 
linsearch(rStorage, D)
convexMaxIndex = np.argmax(rStorage - np.log(rStorage))
print(maxIndex, convexMaxIndex)