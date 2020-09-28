# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 16:29:35 2020

@author: Nicholas Himes
"""

import numpy as np
import matplotlib.pyplot as plt

#%% Given Case
def toyStockSimulator(h):
    N = 100 #100 days
    S1p = [1]*(N+1)
    S2p = [1,2]*int((N/2)+1)
    
    money = 1 #Start with $1
    
    r = [money] #Returns
    #Start of each day, invest h proportions of total money into the stocks
    
    for day in range(1,N+1): #Start on the second day
        Xd1 = S1p[day] / S1p[day-1]
        Xd2 = S2p[day] / S2p[day-1]
        r1 = Xd1 * h[0] * money
        r2 = Xd2 * h[1] * money
        money = r1 + r2
        r.append(money)
        
    return r

givenCase = toyStockSimulator([0.5,0.5])
    
print("Money after 100 days:", "${}".format(givenCase[-1]))

#%% Find Optimal h

# Need to try all pairs that add to 1 for h
rStorage = []
for i in np.linspace(0,1,1001): # 0, 0.001, .... 0.999, 1  (size 1001)
    rStorage.append(toyStockSimulator([i,1-i])[-1])

maxMoney = max(rStorage)
maxIndex = rStorage.index(maxMoney)
winningPair = [maxIndex/1000 , (1000-maxIndex)/1000]
print("Optimal h was {} with ${}".format(winningPair, maxMoney))

plt.figure(1)
plt.plot(np.linspace(0,1,1001), rStorage)
plt.xlabel('First h index')
plt.ylabel('R')
plt.title("Toy Example")

