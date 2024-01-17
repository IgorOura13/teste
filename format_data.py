#Format incoming excel files
import pandas as pd
from datetime import datetime, timedelta, time
import re
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
import matplotlib.pyplot as plt
import csv

scaler = MinMaxScaler(feature_range=(0, 1))
def run_format_data(dados_processos, dados_viscosidade):
    #Format time values
    def clean_and_format_time(time_str):
        time_str = str(time_str)

        cleaned_time = re.sub(r'[^\d]', '', time_str)


        if len(cleaned_time) == 1:
            cleaned_time = '0' + cleaned_time


        if len(cleaned_time) == 3:
            hours = cleaned_time[0]
            minutes = cleaned_time[1:]
        elif len(cleaned_time) >= 4:
            hours = cleaned_time[:2]
            minutes = cleaned_time[2:4]
        else:
            return None


        formatted_time = f'{hours.zfill(2)}:{minutes.zfill(2)}'

        return formatted_time

    #Fromat numerical values
    def format_value1(value_str, casas = 1):
        value_str = str(value_str)

        clean = re.sub(r'[^\d]', '', value_str)

        inteiro = clean[:casas]
        decimal = clean[casas:]

        valor_formatado = f'{inteiro}.{decimal}'

        try:
            float_value = float(valor_formatado)
        except ValueError:
            float_value = 0.0
        return float_value

    def format_value0(value_str):
        value_str = str(value_str)
        clean = re.sub(r'[^\d]', '', value_str)
        if len(clean) == 3:
            inteiro = clean[:1]
            decimal = clean[1:]
        elif len(clean) < 3:
            inteiro = 0
            decimal = clean
        valor_formatado = f'{inteiro}.{decimal}'
        valor_formatado = float(valor_formatado)
        return valor_formatado

    #Old data

    for coluna in dados_processos.columns:
        if dados_processos[coluna].dtype == 'object':  # Verifique se a coluna contém texto
            dados_processos[coluna] = dados_processos[coluna].str.replace('"', '')
    dados_processos.columns = dados_processos.columns.str.replace('"', '')

    mudar = {
        "TS" : "Data"
    }

    dados_processos = dados_processos.rename(columns = mudar)
    dados_processos.head()

    mapa = {
        "DATA E HORA" : "Data"
    }
    dados_viscosidade = dados_viscosidade.rename(columns = mapa)
    dados_viscosidade['TQ SUSPENSÃO'] = dados_viscosidade['TQ SUSPENSÃO'].apply(lambda x: ''.join(re.findall(r'\d+', str(x))))

    dados_viscosidade = dados_viscosidade.drop(["VEL_1_RPM", "COZEDOR", "ASPECTO", " ID"], axis=1)

    pd.set_option('display.max_columns', None)

    dados_processos['Data'] = pd.to_datetime(dados_processos['Data'], utc = True)
    dados_viscosidade['Data'] = pd.to_datetime(dados_viscosidade['Data'], utc = True)


    lista_variaveisformat = ['Dosagem_Acucar_TQ1001', 'Dosagem_Acucar_TQ1002', 'Potencia_Agitador_1605', 'Potencia_Bomba_1006',
                    'Dosagem_Agua_TQ1001', 'Dosagem_Agua_TQ1002', 'Dosagem_Agua_TQ1003', 'Dosagem_Vinagre_TQ1001',
                    'Dosagem_Vinagre_TQ1002', 'Dosagem_Vinagre_TQ1003', 'Vazao_Pasta_PV', 'Temp_Final', 'Temperatura_3_Corpo', 'Temperatura_1_Corpo',
                    'Dosagem_Acucar_TQ1003','Dosagem_Oleo_TQ1001', 'Dosagem_Oleo_TQ1002', 'Dosagem_Oleo_TQ1003',
                    'Pressao_CZ_1603', 'Pressao_CZ_1605', 'Vazao_Pasta_CV', 'Temp_Holding_1633', 'Temp_Holding_1634',
                    'Corrente_Agitador_1601', 'Corrente_Agitador_1602', 'Corrente_Agitador_1603', 'Corrente_Agitador_1604',
                    'Corrente_Agitador_1605', 'Corrente_BB_1006', 'Corrente_Bomba_1601', 'Corrente_Bomba_1602']

    for var in lista_variaveisformat:
        dados_processos[var] = dados_processos[var].apply(format_value1)

    dados_processos.iloc[0:, 1:]=scaler.fit_transform(dados_processos.iloc[0:, 1:].to_numpy())
    dados_viscosidade['TQ SUSPENSÃO'] = pd.to_numeric(dados_viscosidade['TQ SUSPENSÃO'], errors='coerce')
    dados_viscosidade[['TQ SUSPENSÃO',' TEMP AMOSTRA C°']]=scaler.fit_transform(dados_viscosidade[['TQ SUSPENSÃO',' TEMP AMOSTRA C°']].to_numpy())
    dados_viscosidade[[' VEL_5_RPM']]=scaler.fit_transform(dados_viscosidade[[' VEL_5_RPM']].to_numpy())

    # Adicione 4 minutos a cada valor na coluna 'DataHora'
    dados_processos['Data'] = dados_processos['Data'] + pd.Timedelta(minutes=4)

    dados_total = pd.merge(dados_processos,
                        dados_viscosidade, how = 'inner', on = 'Data')
    return dados_total

def inverse_scale(input):
    
    scale_df = pd.DataFrame(scaler.inverse_transform(input))
    return scale_df
