# Inpiration for this script found at https://data.world/bgp12/nbancaacomparisons/
# Ben Pierce's scraping methodology was adapted and expanded to work with a much larger NCAA dataset.


import numpy as np
import pandas as pd
from bs4 import BeautifulSoup, SoupStrainer
import sys
import string
import requests
import datetime
import progressbar
import time
import re

def player_basic_info():
    players = []
    base_url = 'https://www.sports-reference.com/cbb/players/'
    end_string = '-index.html'

    # iterate through all last name starting letters
    for letter in string.ascii_lowercase:
        page_request = requests.get(base_url + letter + end_string)
        soup = BeautifulSoup(page_request.text,"lxml")
        # find all links on page
        links = soup.find("div", { "class" : "index" }).find_all("a")

        # store common element of all player page urls as string
        player_check = '/cbb/players/'

        # define variable to store all results for current last name starting letter
        current_letter_players = []

        # iterate through links
        for link in links:
            temp_url = link['href']
            # check if link is player link. if so, store info
            if player_check in temp_url:
                player_name = link.text
                player_entry = {'url': temp_url,
                                'name': player_name}
                current_letter_players.append(player_entry)
        # make current letter list into a dataframe, then append it to players
        df = pd.DataFrame(current_letter_players)
        players.append(df)
        
    return players

def player_info(url):
    # define all quantities
    height = None
    games = None
    fgpg = None
    fgapg = None
    fgpct = None
    ftpg = None
    ftapg = None
    ftpct = None
    trbpg = None
    pfpg = None
    ptspg = None
    sospg = None

    # define base url
    cbb_url = 'https://www.sports-reference.com/'

    # request and read-in player stat page
    page_request = requests.get(cbb_url + str(url))
    soup = BeautifulSoup(page_request.text,"lxml")

    # pull player height from page
    if soup.find(itemprop="height") != None:
        height = str(soup.find(itemprop="height").text)

    # find first table to get per-game stats
    table = soup.find('table')

    # check table presence before accessing it
    if table:
        # find the footer section of the table
        table_foot = table.find('tfoot')

        # iterate through the footer
        for row in table_foot.findAll('tr'):
            cells  = row.findAll('td')
            playerData = str(cells) #the indexes are not uniform across the database

            # pull each career value from the table footer section
            games = re.search(r'data-stat="g">(.*?)</td>', playerData).group(1) 
            fgpg = re.search(r'data-stat="fg_per_g">(.*?)</td>', playerData).group(1)
            fgapg = re.search(r'data-stat="fga_per_g">(.*?)</td>', playerData).group(1)
            fgpct = re.search(r'data-stat="fg_pct">(.*?)</td>', playerData).group(1)
            ftpg = re.search(r'data-stat="ft_per_g">(.*?)</td>', playerData).group(1)
            ftapg = re.search(r'data-stat="fta_per_g">(.*?)</td>', playerData).group(1)
            ftpct = re.search(r'data-stat="ft_pct">(.*?)</td>', playerData).group(1)
            trbpg = re.search(r'data-stat="trb_per_g">(.*?)</td>', playerData).group(1)
            pfpg = re.search(r'data-stat="pf_per_g">(.*?)</td>', playerData).group(1)
            ptspg = re.search(r'data-stat="pts_per_g">(.*?)</td>', playerData).group(1)
            sospg = re.search(r'data-stat="sos">(.*?)</td>', playerData).group(1)

            break  #bad but I want the structure to remain the same in case I want more data outside overall stats
                # try and pull all leagues the player was in

    # store each called value into a dictionary
    player_entry = {'height': height,
                    'games': games,
                    'fgpg': fgpg,
                    'fgapg': fgapg,
                    'fgpct': fgpct,
                    'ftpg': ftpg,
                    'ftapg': ftapg,
                    'ftpct': ftpct,
                    'trbpg': trbpg,
                    'pfpg': pfpg,
                    'ptspg': ptspg,
                    'sospg': sospg}

    return player_entry


######################################################################################
#MAIN 
# generate base string for file location
names_base_path = 'ncaa_scrapes/names_urls/'

# generate list of letters in the alphabet
alphabet_list = list(string.ascii_lowercase)

# call function that scrapes all player names and statpage urls
players_general_info = player_basic_info()
print('General info/player url loaded...')

# define counter variable to keep track of scraping progress
counter = 1

# iterate through each set of players and writes the names/urls to a csv
for i in range(0,26):
    # generate full path string
    url_save_location = names_base_path + alphabet_list[i] + '_names_urls.csv'

    # write current letter players to csv, named appropriately
    name_df = players_general_info[i]
    name_df.to_csv(url_save_location, index=False) 

    # define df for stat scraping
    stats_df = pd.DataFrame()

    # iterate through player urls in each dataframe
    for j,url in enumerate(name_df.url):
        
        # scrape current player url to pull player stats
        player = player_info(url)

        # append current player stats to stats_df
        stats_df = stats_df.append(player, ignore_index= True)

        # print current counter value and update 
        print(counter)
        counter += 1

        # sleep the scraping to avoid triggering ddos protections
        time.sleep(0.1)

    # define path for saving current stats df as csv
    stats_save_location = 'ncaa_scrapes/player_stats/' + alphabet_list[i] + '_player_stats.csv'

    # write current player stats df to csv
    stats_df.to_csv(stats_save_location, index=False)

    # concatenate name and stats df
    name_stats_df = pd.concat([name_df, stats_df], axis=1)

    # define path for merged df and write it to csv
    names_stats_save_location = 'ncaa_scrapes/names_merge_stats/' + alphabet_list[i] + '_name_stats.csv'
    name_stats_df.to_csv(names_stats_save_location, index=False)
#players_general_info.to_csv('ncaa_test.csv', index=False)

######################################################################################
