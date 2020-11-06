# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 18:31:42 2020

@author: Nicholas Himes
"""

#%% File Description
# This file has examples on how to use the nba_api to gather data

# Look at https://github.com/swar/nba_api/tree/master/nba_api/stats static and endpoints libraries!

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

#%% Cool Functions
def yearConvert(startYear):
    #Given year like 2003, returns "2003-04" for use in file calling
    ans = str(startYear) + "-"
    secondYear = startYear + 1 - 2000
    if secondYear < 10: #Its a single digit
        ans += "0"
    ans += str(secondYear)
    return ans

#%% nba_api Examples
career = playercareerstats.PlayerCareerStats(player_id='203076')
ADcareer = career.season_totals_regular_season.get_data_frame()
ADplayoffs = career.season_totals_post_season.get_data_frame()

lebron = players.find_players_by_full_name('Lebron James')
lebronOrLove = players.find_players_by_last_name('^(james|love)$')

allPlayers = players.get_players() #All players ever
activePlayers = players.get_active_players()
for player in allPlayers:
    if player["full_name"] == "LeBron James":
        lebronsID = player["id"]
career = playercareerstats.PlayerCareerStats(player_id='{}'.format(lebronsID))
lebronCareer = career.season_totals_regular_season.get_data_frame()
lebronPlayoffs = career.season_totals_post_season.get_data_frame()

lebron_info = commonplayerinfo.CommonPlayerInfo(player_id="{}".format(lebronsID))
lebron_bio = lebron_info.common_player_info.get_data_frame() #Draft position, hometown, height, weight, etc

allTeams = teams.get_teams() #Team names and IDs
for l in allTeams:
    if l["full_name"] == "Los Angeles Lakers":
        lakersID = l["id"]

lakersRoster = commonteamroster.CommonTeamRoster(lakersID, season="2019-20")
lakersRosterData = lakersRoster.common_team_roster.get_data_frame()

standings19_20 = leaguestandingsv3.LeagueStandingsV3(season="2019-20")
standings19_20data = standings19_20.get_data_frames()[0] #Can get regular season team stats (WL Record) from this

#%% Basketball-Reference Examples
stevosAdvanced = pd.DataFrame()
for year in range(2000,2020): #Search for the big kiwi in all data
    temp = pd.read_excel("./Basketball-Reference/advanced{}.xlsx".format(yearConvert(year)))
    for index, row in temp.iterrows():
        if "Steven Adams" in row["Player"]:
            stevo = row
            stevo["Year"] = yearConvert(year)
            stevosAdvanced = stevosAdvanced.append(stevo, ignore_index=True)
            
print(stevosAdvanced[['Year','Age','WS/48','VORP']])
            
# Plot how well OKC has done in playoffs every year
OKCplayoffRankings = {}
for year in range(2000,2020): #Year goes to 2019, but playoffs in 2020 so +1 to rankings list years
    temp = pd.read_excel("./Basketball-Reference/playoffs{}.xlsx".format(yearConvert(year)), header=1)
    OKCplayoffRankings[year+1] = None
    for index, row in temp.iterrows():
        if "Thunder" in row["Team"]:
            OKCplayoffRankings[year+1] = row["Rk"]
plt.figure()
yearKeys = list(OKCplayoffRankings.keys())
plt.stem(yearKeys,list(OKCplayoffRankings.values()), bottom=16)
plt.ylim([17, 0])
plt.title("OKC Final Playoff Rankings")
plt.xlabel("Playoff Years")
yearLabels = []
for y in yearKeys:
    if y % 4 == 0:
        yearLabels.append(y)
    else:
        yearLabels.append(None)
plt.xticks(yearKeys, labels=yearLabels) #Force x ticks to be integers
plt.ylabel("Rank 1-16")


