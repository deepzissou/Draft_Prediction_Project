# Import our dependencies
import pandas as pd
from sklearn.model_selection import train_test_split
from joblib import dump, load
from sklearn.ensemble import RandomForestClassifier

# define a function that accepts the form dictionary as an input
def predict_from_form(form_data):
    # pull out each value from the input dictionary into its own variable
    name = form_data['name']
    fgapg = form_data['fgapg']
    fgpct = form_data['fgpct']
    fgpg = form_data['fgpg']
    ftapg = form_data['ftapg']
    ftpct = form_data['ftpct']
    ftpg = form_data['ftpg']
    games = form_data['games']
    height = form_data['height']
    pfpg = form_data['pfpg']
    ptspg = form_data['ptspg']
    sospg = form_data['sospg']
    trbpg = form_data['trbpg']

    # import the saved rfc model
    model = load('pro_predict_model.joblib')

    # collect all stats into a list
    stat_list = [fgapg, fgpct, fgpg, ftapg, ftpct, ftpg, games, height, pfpg, ptspg, sospg, trbpg]

    # turn stats into 2d array with stat names
    stat_names = ['fgapg', 'fgpct', 'fgpg', 'ftapg', 'ftpct', 'ftpg', 'games', 'height', 'pfpg', 'ptspg', 'sospg', 'trbpg']
    temp_dict = {stat_names[i]:stat_list[i] for i in range(len(stat_names))}
    temp_df = pd.DataFrame(temp_dict, index=[0])
    input_array = [temp_df.loc[0,:]]

    # run the stats through the model
    output = model.predict(input_array)
    result_val = output[0]

    # use conditional statements to set appropriate response based on model output
    if result_val == 0:
        response_string = f"Player {name} is not predicted to play Basketball professionally based on their career stats."
    elif result_val == 1:
        response_string = f"Player {name} is predicted to play Basketball professionally."

    # return the text response 
    return response_string