# External libraries
import pandas as pd
from io import BytesIO
import streamlit as st
import inspect
import shap
import streamlit.components.v1 as components

# Converting dataframe to xlsx file

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

# Showing the code of the function

def show_code(func, extra = ''):
    sourcelines, _ = inspect.getsourcelines(func)
    st.code(extra+"".join(sourcelines[1:]))

def one_hot_for_prediction(input):

    columns = [
    'Sodium_hydroxide',
    'Sodium_carbonate',
    'Water',
    'Fragance',
    'Blue_dye',
    '%_Active',
    '%_Sodium_percarbonate',
    'Dosage',
    'Time_of_contact_(min)',
    'Temperature',
    'Active_0',
    'Active_1',
    'Active_2',
    'Active_3',
    'Active_4',
    'Active_5',
    'Active_6',
    'Active_7',
    'Active_8',
    'Test_1',
    'Test_2',
    'Test_3',
    'Test_4',
    'Test_5',
    'Test_6',
    'Test_7'
    ]

    one_hot_df = dict(zip(columns, [0]*26))
    size = len(input)
    one_hot_df['Sodium_hydroxide'] = [0]*size
    one_hot_df = pd.DataFrame(one_hot_df)

    def encode_active(input):
        lista = [0]*9
        lista[input] = 1
        return lista
    def encode_test(input):
        lista = [0]*7
        lista[input - 1] = 1
        return lista

    for index, row in enumerate(input.values):
        list_row = row.tolist()
        active_value = list_row.pop(0)
        test_value = list_row.pop(7)
        active_value = encode_active(int(active_value))
        test_value = encode_test(int(test_value))
        list_row = list_row + active_value + test_value
        one_hot_df.loc[index] = list_row

    return one_hot_df

def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)