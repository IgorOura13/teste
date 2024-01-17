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


def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)
