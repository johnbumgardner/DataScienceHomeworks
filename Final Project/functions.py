# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 13:17:36 2020

@author: Nicholas Himes
"""


#%% Imports
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import leaguestandingsv3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from sklearn import linear_model
from sklearn.metrics import mean_squared_error

#%% Cool Functions
def yearConvert(startYear):
    #Given year like 2003, returns "2003-04" for use in file calling
    ans = str(startYear) + "-"
    secondYear = startYear + 1 - 2000
    if secondYear < 10: #Its a single digit
        ans += "0"
    ans += str(secondYear)
    return ans

def train_test(x, y, teamEverything, trainRatio):
    
    everythingNoNones = teamEverything[[x,y]].mask(teamEverything[[x,y]].eq(None)).dropna()
    # print(everythingNoNones)
    
    trainAmount = int(trainRatio * len(everythingNoNones[x]))
    
    xTrain = everythingNoNones[x][:trainAmount].values.reshape(-1,1) #15 Seasons
    xTest = everythingNoNones[x][trainAmount:].values.reshape(-1,1) #5 Seasons
    yTrain = everythingNoNones[y][:trainAmount].values.reshape(-1,1)
    yTest = everythingNoNones[y][trainAmount:].values.reshape(-1,1)
    
    # print(xTrain)
    # print(xTest)
    # print(yTrain)
    # print(yTest)
    
    regr = linear_model.LinearRegression()
    regr.fit(xTrain, yTrain)
    
    yPred = regr.predict(xTest)
    
    MSE = mean_squared_error(yTest, yPred)
    
    return xTest, yPred, MSE, everythingNoNones