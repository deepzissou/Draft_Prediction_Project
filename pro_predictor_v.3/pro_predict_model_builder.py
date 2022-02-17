# Import our dependencies
import pandas as pd
from sklearn.model_selection import train_test_split
from joblib import dump, load
from sklearn.ensemble import RandomForestClassifier

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

# define dataset
# Feautures and Predicted
X =train[['fgapg','fgpct','fgpg','ftapg','ftpct','ftpg','games','height','pfpg','ptspg','sospg','trbpg']]
y = train['is_pro'].astype(int)

# define the model
model = RandomForestClassifier()

# fit the model
model.fit(X, y)

# dump the trained model to an external, loadable file
dump(model, 'pro_predict_model.joblib')