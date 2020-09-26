# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 14:38:30 2020

@author: Nicholas Himes
"""


import numpy as np
import pandas as pd

#%% Function
def assetPrices(PricesDF, h):
    N = 2517 #Size of the Stanford Dataset
    
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

#%% Import Data
df = pd.read_csv("asset_prices.csv")

#%% Task 2 - Compute the optimal h for D = 2.
h = [0.5, 0.5]
r = assetPrices(df.iloc[:,:2]) #Give it the first two columns of stocks




#%% Task 3 - Compute the optimal h for D = 3.

