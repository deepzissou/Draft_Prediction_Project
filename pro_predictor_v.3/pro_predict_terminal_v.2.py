# Import our dependencies
import pandas as pd
from sklearn.model_selection import train_test_split
from joblib import dump, load
from sklearn.ensemble import RandomForestClassifier

# load the previously trained model
model = load('pro_predict_model.joblib')

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