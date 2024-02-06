# External libraries
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectFromModel
from sklearn.pipeline import Pipeline


# SAVED INFO
visc_path = "data_visc.csv"
proc_path = "data_proc.csv"
model_path = 'pipeline_model.sav'
def model():
    return pickle.load(open('pipeline_model.sav', 'rb'))

def dataframe(type):
    return pd.read_csv(type, index_col = False)


def inv_scale(column):
    v = dataframe(visc_path)
    df_max = max(v[" VEL_5_RPM"].max(), column.max())
    df_min = min(v[" VEL_5_RPM"].min(), column.min())
    new_column = column*(df_max - df_min) + df_min
    return new_column


def check_and_drop_missing_rows(df):
    # Check if there are any missing values in the DataFrame
    if df.isnull().values.any():
        # If missing values are found, drop rows with missing values
        df = df.dropna(axis=0)
        print("Rows with missing values have been dropped.")
    else:
        print("No missing values found in the DataFrame.")

    return df
# AUTODEPLOY

def check_data(input_v, input_p):
    old_df_v = dataframe(visc_path)
    old_df_p = dataframe(proc_path)
    new_df_v = input_v
    new_df_p = input_p
    new_dfs = [new_df_v, new_df_p]
    old_dfs = [old_df_v, old_df_p]
    
    errors = []
    for i in range(len(new_dfs)):
        if len(old_dfs[i].keys()) == len(new_dfs[i].keys()):
            for index, value in enumerate(list(old_dfs[i].keys() == new_dfs[i].keys())):
                if value == False:
                    error_type = f"The '{new_dfs[i].keys()[index]}' column is either out of order or written incorrectly."
                    errors.append(error_type)
        else:
            error_type = "Different number of columns"
            errors.append(error_type)
    if errors != []:
        warning = "The correct columns pattern is:"
        return (errors, warning)
    return True

def new_df(df, type):
    old_df = dataframe(type)
    new_df = pd.concat([old_df, df])
    return new_df

def tank(input):

    dados_total = input

    dados_total['TQ SUSPENSÃO'] = dados_total['TQ SUSPENSÃO'].replace({0.5: 1002, 0.0: 1001, 1.0: 1003})
    dados_total['TQ SUSPENSÃO'] = dados_total['TQ SUSPENSÃO'].map('{:.0f}'.format)
    dados_total.head()
    def escolher_valor_acucar(row):
        if row['TQ SUSPENSÃO'] == '1001':
            return row['Dosagem_Acucar_TQ1001']
        elif row['TQ SUSPENSÃO'] == '1002':
            return row['Dosagem_Acucar_TQ1002']
        elif row['TQ SUSPENSÃO'] == '1003':
            return row['Dosagem_Acucar_TQ1003']
        else:
            return None

    dados_total['Dosagem_Acucar'] = dados_total.apply(escolher_valor_acucar, axis=1)
    dados_total = dados_total.drop(columns=['Dosagem_Acucar_TQ1001', 'Dosagem_Acucar_TQ1002', 'Dosagem_Acucar_TQ1003'])
    def escolher_valor_agua(row):
        if row['TQ SUSPENSÃO'] == '1001':
            return row['Dosagem_Agua_TQ1001']
        elif row['TQ SUSPENSÃO'] == '1002':
            return row['Dosagem_Agua_TQ1002']
        elif row['TQ SUSPENSÃO'] == '1003':
            return row['Dosagem_Agua_TQ1003']
        else:
            return None

    dados_total['Dosagem_Agua'] = dados_total.apply(escolher_valor_agua, axis=1)
    dados_total = dados_total.drop(columns=['Dosagem_Agua_TQ1001', 'Dosagem_Agua_TQ1002', 'Dosagem_Agua_TQ1003'])
    def escolher_valor_oleo(row):
        if row['TQ SUSPENSÃO'] == '1001':
            return row['Dosagem_Oleo_TQ1001']
        elif row['TQ SUSPENSÃO'] == '1002':
            return row['Dosagem_Oleo_TQ1002']
        elif row['TQ SUSPENSÃO'] == '1003':
            return row['Dosagem_Oleo_TQ1003']
        else:
            return None

    dados_total['Dosagem_Oleo'] = dados_total.apply(escolher_valor_oleo, axis=1)
    dados_total = dados_total.drop(columns=['Dosagem_Oleo_TQ1001', 'Dosagem_Oleo_TQ1002', 'Dosagem_Oleo_TQ1003'])
    def escolher_valor_vinagre(row):
        if row['TQ SUSPENSÃO'] == '1001':
            return row['Dosagem_Vinagre_TQ1001']
        elif row['TQ SUSPENSÃO'] == '1002':
            return row['Dosagem_Vinagre_TQ1002']
        elif row['TQ SUSPENSÃO'] == '1003':
            return row['Dosagem_Vinagre_TQ1003']
        else:
            return None

    dados_total['Dosagem_Vinagre'] = dados_total.apply(escolher_valor_vinagre, axis=1)
    dados_total = dados_total.drop(columns=['Dosagem_Vinagre_TQ1001', 'Dosagem_Vinagre_TQ1002', 'Dosagem_Vinagre_TQ1003'])
    return dados_total

def train_model(input):

    df = input
    
    X = df.drop(["Data", "TQ SUSPENSÃO", " VEL_5_RPM"], axis=1)
    y = df[" VEL_5_RPM"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Machine Learning model
    # Criar o pipeline
    pipeline = Pipeline([
        ('feature_selection', SelectFromModel(RandomForestRegressor(random_state=42))),
        ('regressor', RandomForestRegressor(random_state=42))
    ])
    # Treinar o modelo
    pipeline.fit(X_train, y_train)

    # Serializing the model with pickle

    pickle.dump(pipeline, open(model_path, 'wb'))
    new_model = open(model_path, 'rb')

    return new_model

def predict(df):
    input_df = df.drop(["Data", "TQ SUSPENSÃO", " VEL_5_RPM"], axis=1)
    pipeline = model()
    predictions = pipeline.predict(input_df)
    df['Predictions_VEL_5_RPM'] = predictions
    return df
# DASHBOARD

