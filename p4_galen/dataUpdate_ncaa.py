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

# define function for updating ncaa player scrapes, wholesale
def player_name_stats_update():

    # initialize counter for scraping
    counter = 1

    # generate base string for names/urls csv file location
    names_base_path = 'ncaa_scrapes/names_urls/'
    names_path_end = '_names_urls.csv'

    # generate base string for stats csv file location
    stats_base_path = 'ncaa_scrapes/player_stats/'
    stats_path_end = '_player_stats.csv'

    # generate base string for names/urls/stats csv file location
    merge_base_path = 'ncaa_scrapes/names_merge_stats/'
    merge_path_end = '_name_stats.csv'

    # generate list of letters in the alphabet
    alphabet_list = list(string.ascii_lowercase)

    # iterate through each player name/url csv by last name starting letter
    for letter in alphabet_list:

        # define path for old player names csv
        names_full_path = names_base_path + letter + names_path_end

        # read in old player names/urls csv and pull urls into a list
        old_names_df = pd.read_csv(names_full_path)
        old_urls = old_names_df['url'].tolist()

        # define dataframe for new player names/urls
        new_player_names_df = pd.DataFrame()

        # define url for player index to be scraped
        player_index_url = 'https://www.sports-reference.com/cbb/players/' + letter + '-index.html'

        # pull all links on index page
        page_request = requests.get(player_index_url)
        soup = BeautifulSoup(page_request.text,"lxml")
        links = soup.find("div", { "class" : "index" }).find_all("a")

        # store common element of all player page urls as string
        player_check = '/cbb/players/'

        # iterate through links
        for link in links:
            temp_url = link['href']

            # confirm link is to player page, if so, build new player name/url entry
            if player_check in temp_url:
                player_name = link.text
                player_name_entry = {'url': temp_url,
                                     'name': player_name}

                # check if player link is new, if so, put it in the new player name dataframe
                if temp_url not in old_urls:
                    new_player_names_df.append(player_name_entry)

        # import player stat scraping function from dataget-ncaa.py
        from dataget_ncaa import player_info

        # define dataframe for new player stats
        new_stats_df = pd.DataFrame()

        # iterate through each new player url
        for k,url in enumerate(new_player_names_df.url):

            # scrape new player stats
            new_player_stats = player_info(url)

            # append new player stats to dataframe
            new_stats_df = new_stats_df.append(new_player_stats, ignore_index= True)

            # print counter and increment the value
            print(counter)
            counter += 1

            # sleep the scraping to avoid triggering ddos protections
            time.sleep(0.1)

        # concatenate new names/urls and stats dataframes
        new_merge_df = pd.concat([new_player_names_df, new_stats_df], axis=1)
        
        # define path for old stats csv
        stats_full_path = stats_base_path + letter + stats_path_end
        
        # read in old stats csv
        old_stats_df = pd.read_csv(stats_full_path)

        # define path for old names/urls/stats csv
        merge_full_path = merge_base_path + letter + merge_path_end

        # read in old names/urls/stats csv
        old_merge_df = pd.read_csv(merge_full_path)

        # concatenate old and new names/urls dataframes
        names_urls_updated_df = old_names_df.append(new_player_names_df, ignore_index=True)

        # concatenate old and new stats dataframes
        stats_updated_df = old_stats_df.append(new_stats_df, ignore_index=True)

        # concatenate old and new names/urls/stats dataframes
        merge_updated_df = old_merge_df.append(new_merge_df, ignore_index=True)

        # overwrite old csv file with updated versions
        names_urls_updated_df.to_csv(names_full_path, index=False)
        stats_updated_df.to_csv(stats_full_path, index=False)
        merge_updated_df.to_csv(merge_full_path, index=False)

