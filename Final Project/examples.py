# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 18:31:42 2020

@author: Nicholas Himes
"""

#%% File Description
# This file has examples on how to use the nba_api to gather data


#%% Imports
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
from nba_api.stats.static import teams
from nba_api.stats.endpoints import commonplayerinfo


#%% Examples
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

allTeams = teams.get_teams()
