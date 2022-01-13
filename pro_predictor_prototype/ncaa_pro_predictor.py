# Import our dependencies
import pandas as pd
#%matplotlib inline
#from matplotlib import pyplot as plt
#from sklearn.datasets import make_blobs
#import sklearn as skl
#import tensorflow as tf
#import numpy as np

#from sklearn.decomposition import PCA
#from sklearn.pipeline import Pipeline
#from sklearn.preprocessing import StandardScaler
#from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
#from sklearn.linear_model import LogisticRegression

#from pathlib import Path

# read in full dataset
bb_players = "combined_ncaa_player_stats.csv" ## adjust if the filepath is different
df = pd.read_csv(bb_players)

#drop url column and rows with nan values
df = df.drop(columns=['url'])
df = df.dropna()

#change height into inches 
def parse_ht(ht):
    # format: 7' 0.0"
    ht_ = ht.split("-")
    ft_ = float(ht_[0])
    in_ = float(ht_[1])
    return (12*ft_) + in_
    df["height"] = df["height"].apply(parse_ht(ht))

df["height"] = df["height"].apply(lambda x:parse_ht(x))

#split data set in half to use first half to train model and second half to test our prediction 
train = df.iloc[:38334]
test = df.iloc[38334:]

# import dependencies for random forest classifier
from sklearn.model_selection import train_test_split
#from sklearn.ensemble import RandomForestRegressor
#from sklearn.inspection import permutation_importance
#import shap
from sklearn.ensemble import RandomForestClassifier
#from matplotlib import pyplot

# define dataset
# Feautures and Predicted
X =train[['fgapg','fgpct','fgpg','ftapg','ftpct','ftpg','games','height','pfpg','ptspg','sospg','trbpg']]
y = train['is_pro'].astype(int)

# define the model
model = RandomForestClassifier()

# fit the model
model.fit(X, y)

# define the initial continuation value
continuation = 'y'

# define a list of acceptable continuation values
cont_list = ['y', 'Y', 'yes', 'Yes']

# define string variable for invalid inputs
invalid_response = 'At least one of the given values was invalid, please start over with proper numeric values.'

# print an intro
print('This RFC model examines NCAA Basketball player career per-game stats to predict if they are likely to go pro.')
print('The model was trained on data scraped from https://www.sports-reference.com/cbb/players/ which may be referenced for data format.')
print("Testing indicated an accuracy rate of approximately 96%.")
print('Enter the requested information to receive a prediction for a player of your choice.')

# run a while loop to request player stat inputs and run them through the model
while continuation in cont_list: # so long as the response is some common version of yes, keep running the loop

    # request player name and relevant stats
    p_name = str(input("What is the player's name?"))

    fgapg = input("What is the player's career Field Goal Attempts per Game stat?")
    fgpct = input("What is the player's career Field Goal Percent Stat?")
    fgpg = input("What is the player's career Field Goals per Game stat?")

    ftapg = input("What is the player's career Free Throw Attempts per Game stat?")
    ftpct = input("What is the player's career Free Throw Percent Stat?")
    ftpg = input("What is the player's career Free Throws per Game stat?")

    games = input("How many Games did the player play in during their NCAA career?")
    height = input("What is the player's height in inches?")

    pfpg = input("What is the player's career Personal Fouls per Game stat?")
    ptspg = input("What is the player's career Points per Game stat?")

    sospg = input("What is the player's career Strength of Schedule stat?")
    trbpg = input("What is the player's career Total Rebounds per Game stat?")

    # collect all stats into a list
    stat_list = [fgapg, fgpct, fgpg, ftapg, ftpct, ftpg, games, height, pfpg, ptspg, sospg, trbpg]

    # attempt to convert all stat inputs to floats
    float_list = []

    for stat in stat_list:
        try:
            float_stat = float(stat)
            float_list.append(float_stat)
        except:
            # if any of the values can't convert to float, the model won't run so restart data entry
            print(invalid_response)
            break

    # turn stats into 2d array with stat names
    stat_names = ['fgapg', 'fgpct', 'fgpg', 'ftapg', 'ftpct', 'ftpg', 'games', 'height', 'pfpg', 'ptspg', 'sospg', 'trbpg']
    try:
        temp_dict = {stat_names[i]:float_list[i] for i in range(len(stat_names))}
    except:
        continue
    
    temp_df = pd.DataFrame(temp_dict, index=[0])
    input_array = [temp_df.loc[0,:]]
    
    # run the stats through the model
    output = model.predict(input_array)
    result_val = output[0]

    # print the result of the prediction
    if result_val == 0:
        print(f"Player {p_name} is not predicted to play Basketball professionally based on their career stats.")
    elif result_val == 1:
        print(f"Player {p_name} is predicted to play Basketball professionally.")

    # confirm if the user wants to continue to another player
    continuation = input("Would you like to predict for another player?")

# print a statement indicating the end of the script
print("Done.")


####################################################
# Notes for revision:
# 1. Clean up unnecessary legacy imports - partially done
# 2. Make it so one invalid entry doesn't force you to restart, preferably without a dozen for loops
# 3. Figure out a cleaner way to get the 2d array the model wants as an input 