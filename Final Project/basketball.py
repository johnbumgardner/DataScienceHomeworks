# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 17:36:51 2020

@author: Nicholas Himes
"""

#%% File Description
# This file is our project's main script and will run through all
# aspects of what we aim to do


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

from functions import yearConvert
from functions import train_test

#%% Main

NBA = ["Hawks","Celtics","Nets","Hornets","Bulls",
       "Cavaliers","Mavericks","Nuggets","Pistons",
       "Warriors","Rockets","Pacers","Clippers",
       "Lakers","Grizzlies","Heat","Bucks","Timberwolves",
       "Pelicans","Knicks","Thunder","Magic","76ers",
       "Suns","Trail Blazers","Kings","Spurs","Raptors",
       "Jazz","Wizards"]
allMSECorr = pd.DataFrame()

for teamInput in NBA:
    #%% Choose a team 
    
    #teamInput = "Rockets"
    
    teamID = None #This teamID is used with nba_api
    allTeams = teams.get_teams() #Team names and IDs
    for l in allTeams:
        if teamInput in l["full_name"]: 
            teamID = l["id"] 
            teamAbbreviation = l["abbreviation"] #Ex ATL for the hawks
    if teamID == None:
        print("No team was found with this name in the years 2000-2020")
    #print(teamID)
    
    #%% Get the team's playoff rank (1-16th place in playoff results)
    teamPlayoffRankings = {}
    for year in range(2000,2020): 
        temp = pd.read_excel("./Basketball-Reference/playoffs{}.xlsx".format(yearConvert(year)), header=1)
        teamPlayoffRankings[yearConvert(year)] = None
        for index, row in temp.iterrows():
            if teamInput in row["Team"]:
                teamPlayoffRankings[yearConvert(year)] = row["Rk"]
                
    #%% Get the team's regular season win percentage
    
    # This dictionary was made once and saved instead of being created fresh every time
    # to avoid timeout punishments from the NBA stats website
    allRegularSeasonStandings = np.load("allRegularSeasonStandings.npy", allow_pickle="TRUE").item()
        
    teamRegularSeasonStandings = {}
    for year, standingsData in allRegularSeasonStandings.items():
        for index, row in standingsData.iterrows():
            if teamInput in row["TeamName"]: #Change to teamID == row["TeamID"] to see technical team data (Ex Seattle+OKC has same ID)
                teamRegularSeasonStandings[year] = row
                
    teamRegularSeasonWinPercentages = {}
    for year, seasonSeries in teamRegularSeasonStandings.items():
        teamRegularSeasonWinPercentages[year] = seasonSeries["WinPCT"]
                
    #%% Get the team's roster for every year
    teamAllRosters = {}
    for year in range(2000,2020):
        time.sleep(2) #Needed to avoid timeouts
        teamRoster = commonteamroster.CommonTeamRoster(teamID, season=yearConvert(year))
        teamRosterData = teamRoster.common_team_roster.get_data_frame()
        teamAllRosters[yearConvert(year)] = teamRosterData
    
    #%% Get advanced stats for each player on the roster every year
    teamAdvancedStats = {}
    for year, rosterDF in teamAllRosters.items():
        #For that year, make a DataFrame with all Advanced Stats for each player
        currentYearDF = pd.DataFrame()
        advanced = pd.read_excel("./Basketball-Reference/advanced{}.xlsx".format(year))
        for advancedIndex, advancedRow in advanced.iterrows():
            for rosterIndex, rosterRow in rosterDF.iterrows():
                if rosterRow["PLAYER"] in advancedRow["Player"]:
                    if advancedRow["Tm"] == teamAbbreviation: 
                        # ^^ Removes stats from players not recorded on that team
                        # Ex) Covington's MIN stats and his TOT (total) stats removed from HOU advanced stats 2019-20
                        currentYearDF = currentYearDF.append(advancedRow, ignore_index=True)
                    elif ((teamAbbreviation=="BKN") and (advancedRow["Tm"] == "BRK")):
                        currentYearDF = currentYearDF.append(advancedRow, ignore_index=True)
                    elif ((teamAbbreviation=="PHX") and (advancedRow["Tm"] == "PHO")):
                        currentYearDF = currentYearDF.append(advancedRow, ignore_index=True)
                    elif ((teamAbbreviation=="CHA") and (advancedRow["Tm"] == "CHO")):
                        currentYearDF = currentYearDF.append(advancedRow, ignore_index=True)
        if not currentYearDF.empty:    
            teamAdvancedStats[year] = currentYearDF
        
    #%% Get summary of advanced stats for every year for the team
    # Will gather WS (Win Shares), OBPM, DBPM, BPM (Box Plus-Minus), 
    # VORP (Value over Replacement Player), and PER (Player Effeciency Rating)
    teamAdvancedSummary = {}
    for year, advancedDF in teamAdvancedStats.items():
        currentYearDF = pd.DataFrame()
        #Normalizing WS Sum by Games Played / Games in Season
        WSnormalizeFactor = 82 / (teamRegularSeasonStandings[year]["WINS"] + teamRegularSeasonStandings[year]["LOSSES"])
        currentYearDF["WS Sum Normalized"] = [sum(advancedDF["WS"]) * WSnormalizeFactor]
        
        currentYearDF["OBPM Sum > 200 MP"] = sum(advancedDF[advancedDF["MP"] > 200]["OBPM"])
        currentYearDF["DBPM Sum > 200 MP"] = sum(advancedDF[advancedDF["MP"] > 200]["DBPM"])
        currentYearDF["BPM Sum > 200 MP"] = sum(advancedDF[advancedDF["MP"] > 200]["BPM"])
        
        #VORP is an almost normalized version of BPM over minutes played by that specific player
        currentYearDF["VORP Sum"] = sum(advancedDF["VORP"])
    
        currentYearDF["PER Sum > 200 MP"] = sum(advancedDF[advancedDF["MP"] > 200]["PER"])
        
        teamAdvancedSummary[year] = currentYearDF
    
    
    #%% Now combine everything into a DF for the team
    
    teamEverything = pd.DataFrame()
    for year in range(2000,2020):
        season = yearConvert(year)
        currentYearDF = pd.DataFrame()
        
        currentYearDF["Season"] = [season]
        currentYearDF["RS Win %"] = teamRegularSeasonWinPercentages[season]
        currentYearDF["Playoff Rank"] = teamPlayoffRankings[season]
        
        currentYearDF["WS Sum Normalized"] = teamAdvancedSummary[season]["WS Sum Normalized"]
        currentYearDF["OBPM Sum > 200 MP"] = teamAdvancedSummary[season]["OBPM Sum > 200 MP"]
        currentYearDF["DBPM Sum > 200 MP"] = teamAdvancedSummary[season]["DBPM Sum > 200 MP"]
        currentYearDF["BPM Sum > 200 MP"] = teamAdvancedSummary[season]["BPM Sum > 200 MP"]
        currentYearDF["VORP Sum"] = teamAdvancedSummary[season]["VORP Sum"]
        currentYearDF["PER Sum > 200 MP"] = teamAdvancedSummary[season]["PER Sum > 200 MP"]
        
        teamEverything = teamEverything.append(currentYearDF, ignore_index=True)
    
    
    #%% Plot & Fit Stuff
    trainRatio = 0.75 #75% of total length after None values removed
    
    teamMSECorr = pd.DataFrame()
    teamMSECorr["Team"] = [teamInput]
    
    plt.figure()
    plt.scatter(teamEverything["RS Win %"], teamEverything["Playoff Rank"])
    plt.xlabel("Regular Season Win %")
    plt.xlim([0,1])
    plt.ylabel("Playoff Rank")
    plt.ylim([16,1])
    plt.title("Regular Season vs Playoffs {}".format(teamInput))
    xTest, yPred, MSE, everythingNoNones = train_test("RS Win %", "Playoff Rank", teamEverything, trainRatio)
    plt.plot(xTest, yPred, color="orange")
    print("MSE between RS Win % and Playoff Rank from Linear Regression is {}".format(MSE))
    corr = np.correlate(everythingNoNones["RS Win %"], everythingNoNones["Playoff Rank"])
    teamMSECorr["MSE_RS Win % and Playoff Rank"] = MSE
    teamMSECorr["Corr_RS Win % and Playoff Rank"] = corr[0]
    print("Correlation between RS Win % and Playoff Rank is {}".format(corr))
    print()
    
    # Now subplots for the rest of the variables with plots for both RS % and Playoff Rank
    plt.figure(figsize=(7,7))
    plt.subplot(2,1,1)
    plt.scatter(teamEverything["WS Sum Normalized"], teamEverything["RS Win %"])
    plt.ylabel("Regular Season Win %")
    plt.ylim([0,1])
    plt.title("Win Shares Sum Normalized {}".format(teamInput))
    xTest, yPred, MSE, everythingNoNones = train_test("WS Sum Normalized", "RS Win %", teamEverything, trainRatio)
    plt.plot(xTest, yPred, color="orange")
    print("MSE between WS Sum Normalized and RS Win % from Linear Regression is {}".format(MSE))
    corr = np.correlate(everythingNoNones["WS Sum Normalized"], everythingNoNones["RS Win %"])
    teamMSECorr["MSE_WS Sum Normalized and RS Win %"] = MSE
    teamMSECorr["Corr_WS Sum Normalized and RS Win %"] = corr[0]
    print("Correlation between WS Sum Normalized and RS Win % is {}".format(corr))
    plt.subplot(2,1,2)
    plt.scatter(teamEverything["WS Sum Normalized"], teamEverything["Playoff Rank"])
    plt.xlabel("Win Shares Sum Normalized")
    plt.ylabel("Playoff Rank")
    plt.ylim([16,1])
    xTest, yPred, MSE, everythingNoNones = train_test("WS Sum Normalized", "Playoff Rank", teamEverything, trainRatio)
    plt.plot(xTest, yPred, color="orange")
    print("MSE between WS Sum Normalized and Playoff Rank from Linear Regression is {}".format(MSE))
    corr = np.correlate(everythingNoNones["WS Sum Normalized"], everythingNoNones["Playoff Rank"])
    teamMSECorr["MSE_WS Sum Normalized and Playoff Rank"] = MSE
    teamMSECorr["Corr_WS Sum Normalized and Playoff Rank"] = corr[0]
    print("Correlation between WS Sum Normalized and Playoff Rank is {}".format(corr))
    print()
    
    plt.figure(figsize=(7,7))
    plt.subplot(2,1,1)
    plt.scatter(teamEverything["OBPM Sum > 200 MP"], teamEverything["RS Win %"])
    plt.ylabel("Regular Season Win %")
    plt.ylim([0,1])
    plt.title("OBPM Sum > 200 MP {}".format(teamInput))
    xTest, yPred, MSE, everythingNoNones = train_test("OBPM Sum > 200 MP", "RS Win %", teamEverything, trainRatio)
    plt.plot(xTest, yPred, color="orange")
    print("MSE between OBPM Sum > 200 MP and RS Win % from Linear Regression is {}".format(MSE))
    corr = np.correlate(everythingNoNones["OBPM Sum > 200 MP"], everythingNoNones["RS Win %"])
    teamMSECorr["MSE_OBPM Sum > 200 MP and RS Win %"] = MSE
    teamMSECorr["Corr_OBPM Sum > 200 MP and RS Win %"] = corr[0]
    print("Correlation between OBPM Sum > 200 MP and RS Win % is {}".format(corr))
    plt.subplot(2,1,2)
    plt.scatter(teamEverything["OBPM Sum > 200 MP"], teamEverything["Playoff Rank"])
    plt.xlabel("OBPM Sum > 200 MP")
    plt.ylabel("Playoff Rank")
    plt.ylim([16,1])
    xTest, yPred, MSE, everythingNoNones = train_test("OBPM Sum > 200 MP", "Playoff Rank", teamEverything, trainRatio)
    plt.plot(xTest, yPred, color="orange")
    print("MSE between OBPM Sum > 200 MP and Playoff Rank from Linear Regression is {}".format(MSE))
    corr = np.correlate(everythingNoNones["OBPM Sum > 200 MP"], everythingNoNones["Playoff Rank"])
    teamMSECorr["MSE_OBPM Sum > 200 MP and Playoff Rank"] = MSE
    teamMSECorr["Corr_OBPM Sum > 200 MP and Playoff Rank"] = corr[0]
    print("Correlation between OBPM Sum > 200 MP and Playoff Rank is {}".format(corr))
    print()
    
    plt.figure(figsize=(7,7))
    plt.subplot(2,1,1)
    plt.scatter(teamEverything["DBPM Sum > 200 MP"], teamEverything["RS Win %"])
    plt.ylabel("Regular Season Win %")
    plt.ylim([0,1])
    plt.title("DBPM Sum > 200 MP {}".format(teamInput))
    xTest, yPred, MSE, everythingNoNones = train_test("DBPM Sum > 200 MP", "RS Win %", teamEverything, trainRatio)
    plt.plot(xTest, yPred, color="orange")
    print("MSE between DBPM Sum > 200 MP and RS Win % from Linear Regression is {}".format(MSE))
    corr = np.correlate(everythingNoNones["DBPM Sum > 200 MP"], everythingNoNones["RS Win %"])
    teamMSECorr["MSE_DBPM Sum > 200 MP and RS Win %"] = MSE
    teamMSECorr["Corr_DBPM Sum > 200 MP and RS Win %"] = corr[0]
    print("Correlation between DBPM Sum > 200 MP and RS Win % is {}".format(corr))
    plt.subplot(2,1,2)
    plt.scatter(teamEverything["DBPM Sum > 200 MP"], teamEverything["Playoff Rank"])
    plt.xlabel("DBPM Sum > 200 MP")
    plt.ylabel("Playoff Rank")
    plt.ylim([16,1])
    xTest, yPred, MSE, everythingNoNones = train_test("DBPM Sum > 200 MP", "Playoff Rank", teamEverything, trainRatio)
    plt.plot(xTest, yPred, color="orange")
    print("MSE between DBPM Sum > 200 MP and Playoff Rank from Linear Regression is {}".format(MSE))
    corr = np.correlate(everythingNoNones["DBPM Sum > 200 MP"], everythingNoNones["Playoff Rank"])
    teamMSECorr["MSE_DBPM Sum > 200 MP and Playoff Rank"] = MSE
    teamMSECorr["Corr_DBPM Sum > 200 MP and Playoff Rank"] = corr[0]
    print("Correlation between DBPM Sum > 200 MP and Playoff Rank is {}".format(corr))
    print()
    
    plt.figure(figsize=(7,7))
    plt.subplot(2,1,1)
    plt.scatter(teamEverything["BPM Sum > 200 MP"], teamEverything["RS Win %"])
    plt.ylabel("Regular Season Win %")
    plt.ylim([0,1])
    plt.title("BPM Sum > 200 MP {}".format(teamInput))
    xTest, yPred, MSE, everythingNoNones = train_test("BPM Sum > 200 MP", "RS Win %", teamEverything, trainRatio)
    plt.plot(xTest, yPred, color="orange")
    print("MSE between BPM Sum > 200 MP and RS Win % from Linear Regression is {}".format(MSE))
    corr = np.correlate(everythingNoNones["BPM Sum > 200 MP"], everythingNoNones["RS Win %"])
    teamMSECorr["MSE_BPM Sum > 200 MP and RS Win %"] = MSE
    teamMSECorr["Corr_BPM Sum > 200 MP and RS Win %"] = corr[0]
    print("Correlation between BPM Sum > 200 MP and RS Win % is {}".format(corr))
    plt.subplot(2,1,2)
    plt.scatter(teamEverything["BPM Sum > 200 MP"], teamEverything["Playoff Rank"])
    plt.xlabel("BPM Sum > 200 MP")
    plt.ylabel("Playoff Rank")
    plt.ylim([16,1])
    xTest, yPred, MSE, everythingNoNones = train_test("BPM Sum > 200 MP", "Playoff Rank", teamEverything, trainRatio)
    plt.plot(xTest, yPred, color="orange")
    print("MSE between BPM Sum > 200 MP and Playoff Rank from Linear Regression is {}".format(MSE))
    corr = np.correlate(everythingNoNones["BPM Sum > 200 MP"], everythingNoNones["Playoff Rank"])
    teamMSECorr["MSE_BPM Sum > 200 MP and Playoff Rank"] = MSE
    teamMSECorr["Corr_BPM Sum > 200 MP and Playoff Rank"] = corr[0]
    print("Correlation between BPM Sum > 200 MP and Playoff Rank is {}".format(corr))
    print()
    
    plt.figure(figsize=(7,7))
    plt.subplot(2,1,1)
    plt.scatter(teamEverything["VORP Sum"], teamEverything["RS Win %"])
    plt.ylabel("Regular Season Win %")
    plt.ylim([0,1])
    plt.title("VORP Sum {}".format(teamInput))
    xTest, yPred, MSE, everythingNoNones = train_test("VORP Sum", "RS Win %", teamEverything, trainRatio)
    plt.plot(xTest, yPred, color="orange")
    print("MSE between VORP Sum and RS Win % from Linear Regression is {}".format(MSE))
    corr = np.correlate(everythingNoNones["VORP Sum"], everythingNoNones["RS Win %"])
    teamMSECorr["MSE_VORP Sum and RS Win %"] = MSE
    teamMSECorr["Corr_VORP Sum and RS Win %"] = corr[0]
    print("Correlation between VORP Sum and RS Win % is {}".format(corr))
    plt.subplot(2,1,2)
    plt.scatter(teamEverything["VORP Sum"], teamEverything["Playoff Rank"])
    plt.xlabel("VORP Sum")
    plt.ylabel("Playoff Rank")
    plt.ylim([16,1])
    xTest, yPred, MSE, everythingNoNones = train_test("VORP Sum", "Playoff Rank", teamEverything, trainRatio)
    plt.plot(xTest, yPred, color="orange")
    print("MSE between VORP Sum and Playoff Rank from Linear Regression is {}".format(MSE))
    corr = np.correlate(everythingNoNones["VORP Sum"], everythingNoNones["Playoff Rank"])
    teamMSECorr["MSE_VORP Sum and Playoff Rank"] = MSE
    teamMSECorr["Corr_VORP Sum and Playoff Rank"] = corr[0]
    print("Correlation between VORP Sum and Playoff Rank is {}".format(corr))
    print()
    
    plt.figure(figsize=(7,7))
    plt.subplot(2,1,1)
    plt.scatter(teamEverything["PER Sum > 200 MP"], teamEverything["RS Win %"])
    plt.ylabel("Regular Season Win %")
    plt.ylim([0,1])
    plt.title("PER Sum > 200 MP {}".format(teamInput))
    xTest, yPred, MSE, everythingNoNones = train_test("PER Sum > 200 MP", "RS Win %", teamEverything, trainRatio)
    plt.plot(xTest, yPred, color="orange")
    print("MSE between PER Sum > 200 MP and RS Win % from Linear Regression is {}".format(MSE))
    corr = np.correlate(everythingNoNones["PER Sum > 200 MP"], everythingNoNones["RS Win %"])
    teamMSECorr["MSE_PER Sum > 200 MP and RS Win %"] = MSE
    teamMSECorr["Corr_PER Sum > 200 MP and RS Win %"] = corr[0]
    print("Correlation between PER Sum > 200 MP and RS Win % is {}".format(corr))
    plt.subplot(2,1,2)
    plt.scatter(teamEverything["PER Sum > 200 MP"], teamEverything["Playoff Rank"])
    plt.xlabel("PER Sum > 200 MP")
    plt.ylabel("Playoff Rank")
    plt.ylim([16,1])
    xTest, yPred, MSE, everythingNoNones = train_test("PER Sum > 200 MP", "Playoff Rank", teamEverything, trainRatio)
    plt.plot(xTest, yPred, color="orange")
    print("MSE between PER Sum > 200 MP and Playoff Rank from Linear Regression is {}".format(MSE))
    corr = np.correlate(everythingNoNones["PER Sum > 200 MP"], everythingNoNones["Playoff Rank"])
    teamMSECorr["MSE_PER Sum > 200 MP and Playoff Rank"] = MSE
    teamMSECorr["Corr_PER Sum > 200 MP and Playoff Rank"] = corr[0]
    print("Correlation between PER Sum > 200 MP and Playoff Rank is {}".format(corr))
    print()

    allMSECorr = allMSECorr.append(teamMSECorr, ignore_index=True)





