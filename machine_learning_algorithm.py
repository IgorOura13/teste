# External libraries
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import RandomOverSampler

# SAVED INFO

def model():
    return pickle.load(open('ml_trained_model.sav', 'rb'))

def dataframe():
    return pd.read_csv('data.csv', index_col = False)

# AUTODEPLOY

def check_data(input):
    old_df = dataframe()
    new_df = input
    errors = []
    if len(old_df.keys()) == len(new_df.keys()):
        for index, value in enumerate(list(old_df.keys() == new_df.keys())):
            if value == False:
                error_type = f"The '{new_df.keys()[index]}' column is either out of order or written incorrectly."
                errors.append(error_type)
    else:
        error_type = "Different number of columns"
        errors.append(error_type)
    if errors != []:
        warning = "The correct columns pattern is:"
        return (errors, warning)
    return True

def new_df(df):
    old_df = dataframe()
    new_df = old_df.append(df)
    return new_df

def train_model(input):

    df = input
    
    # Differentiating categorical and numerical variables

    Active_column = df.columns[0]
    Test_column = df.columns[8]
    Final_Result_column = df.columns[-1]

    dic = {
    Active_column: 'category',
    Test_column: 'category',
    Final_Result_column: 'category'
    }

    for i in dic.keys():
        df[i] = df[i].astype("category")
    for i in df.keys():
        if i not in dic.keys():
            df[i] = df[i].astype(float, errors = 'raise')

    # Using one-hot-encoding and dividng data between prediction data and answer

    x = df.drop(Final_Result_column, axis = 1) # Prediction data
    x = pd.get_dummies(x) # Using one-hot-encoding to turn categorical variables into binary
    y = df[Final_Result_column] # Real answer

    # Oversampling

    r_over_samp = RandomOverSampler(random_state=0)
    x_resampled, y_resampled = r_over_samp.fit_resample(x, y)

    x = np.array(x_resampled)
    y = np.array(y_resampled)

    # Machine Learning model

    model = RandomForestClassifier(random_state=42)
    model.fit(x, y)

    # Serializing the model with pickle

    pickle.dump(model, open('ml_trained_model.sav', 'wb'))
    new_model = open('ml_trained_model.sav', 'rb')

    return new_model

# DASHBOARD

