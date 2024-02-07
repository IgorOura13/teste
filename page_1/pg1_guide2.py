# External libraries
import pandas as pd
import streamlit as st
import shap
import warnings
import sklearn
# Internal libraries
from machine_learning_algorithm import model, predict, tank, inv_scale, check_and_drop_missing_rows, dataframe
from utils import st_shap
from format_data import run_format_data
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt

# Dictionaries relating variable's name with its corresponding number

# Columns names for plots

ind = ['Corrente Agitador 1601',
    'Corrente Agitador 1602',
    'Corrente Agitador 1603',
    'Corrente Agitador 1604',
    'Corrente Agitador 1605',
    'Corrente BB 1006',
    'Corrente Bomba 1601',
    'Corrente Bomba 1602',
    'Potência Agitador 1605',
    'Potência Bomba 1006',
    'Vazão Pasta CV',
    'Pressão CZ 1603',
    'Pressão CZ 1605',
    'Vazão Pasta PV',
    'Temperatura Final',
    'Temperatura Holding 1633',
    'Temperatura Holding 1634',
    'Temperatura 3 Corpo',
    'Temperatura 1 Corpo',
    'Temperatura Amostra',
    'Dosagem Açúcar',
    'Dosage Água',
    'Dosagem Óleo',
    'Dosagem Vinagre'
      ]
def run_guide2():
    # Tutorial on uploading a csv file

    with st.expander("TUTORIAL"):
        
        st.write('''
            First off, create a new spreadsheet with Google Sheets including your dataset.\n
            Your file must include only the spreadsheet header and rows.
        ''')
        st.markdown("---")
        st.write("Follow the example below, your spreadsheet must match up to this model for each spreadsheet:")
        st.markdown("---")
        
        st.write("After that, download your CSV or xlsx file")
        
        st.markdown("---")
        st.write("Finally, click the 'Browse files' button to upload your file:")
        st.image("images/tutorial-pg1-foto3.png")
        st.markdown("---")
        st.write("That's it! Now you can perform a prediction!")

    # Uploading a file

    if 'download_pg1_guide3' not in st.session_state:
            st.session_state['download_pg1_guide3'] = False

    try:

        if 'predict_pg1_guide3' not in st.session_state:
            st.session_state['predict_pg1_guide3'] = False
        option_v = st.selectbox('What type of viscosity file?',
            ('CSV', 'Excel'))
        
        option_p = st.selectbox('What type of processes file?',
            ('CSV', 'Excel'))
        
        with st.form("Inputs3"):
            if option_v == 'CSV':
                uploaded_file_v = st.file_uploader("Choose a CSV file for viscosity:", help = "Please enter a CSV viscosity")
                file = True
                if uploaded_file_v is not None: 
                    dataframe_v = pd.read_csv(uploaded_file_v, index_col = False)                  
                    
                else:
                    file = False
            elif option_v == 'Excel':
                uploaded_file_v = st.file_uploader("Choose a xlsx file for viscosity:", help = "Please enter a xlsx viscosity")
                file = True
                if uploaded_file_v is not None: 
                    dataframe_v = pd.read_excel(uploaded_file_v, index_col = False)   
            
            if option_p == 'CSV':
                uploaded_file_p = st.file_uploader("Choose a CSV file for processes:", help = "Please enter a CSV processes file")
                file = True
                if uploaded_file_p is not None: 
                    dataframe_p = pd.read_csv(uploaded_file_p, index_col = False)                  
                    
                else:
                    file = False
            elif option_p == 'Excel':
                uploaded_file_p = st.file_uploader("Choose a xlsx file for processes:", help = "Please enter a xlsx processes file")
                file = True
                if uploaded_file_p is not None: 
                    dataframe_p = pd.read_excel(uploaded_file_p, index_col = False) 

            submitted = st.form_submit_button("Predict")
            

            if submitted:
                if file:     
                    pipeline = model()
                    reg = pipeline.named_steps['regressor']
                    o_dataframe = run_format_data(dataframe_p, dataframe_v, scaled = False)
                    dataframe = run_format_data(dataframe_p, dataframe_v)
                    
                    dataframe = tank(dataframe)
                    dataframe = check_and_drop_missing_rows(dataframe)
                    if " VEL_5_RPM" in dataframe.columns:
                        
                        real = True
                    else:
                        real = False
                    
                    prediction_df = predict(dataframe, real)
                    
                    float_prediction = prediction_df["Predictions_VEL_5_RPM"]
                    dataframe["Predictions_VEL_5_RPM"] = inv_scale(float_prediction)
                    o_dataframe["Predictions_VEL_5_RPM"] = inv_scale(float_prediction)
                    
                    df_xlsx = o_dataframe.to_csv(index = False).encode('utf-8')
                    
                    if 'dataframe' not in st.session_state:
                        st.session_state['dataframe'] = o_dataframe
                    if 'df_xlsx' not in st.session_state:
                        st.session_state['df_xlsx'] = df_xlsx
                    if 'prediction_df' not in st.session_state:
                        st.session_state['prediction_df'] = prediction_df
                    if 'float_prediction' not in st.session_state:
                        st.session_state['float_prediction'] = float_prediction
                    if 'reg' not in st.session_state:
                        st.session_state['reg'] = reg
                    

                    st.session_state['download_pg1_guide3'] = True
                    st.session_state['predict_pg1_guide3'] = True
                    
    except (ValueError, IndexError):
        st.warning("Warning: unable to predict, make sure your file is correct")

    if submitted:
        if not file:
            st.warning("Warning: no file uploaded")

    if st.session_state['predict_pg1_guide3']:

        warnings.filterwarnings("ignore")
        prediction_df = st.session_state['prediction_df']
        float_prediction = st.session_state['float_prediction']
        reg = st.session_state['reg']

        explainer = shap.TreeExplainer(reg)
        new_pred_df = prediction_df.drop(["Data"], axis = 1)
        shap_values = explainer.shap_values(new_pred_df)
        instance_index = st.selectbox('Select Instance Index', range(len(new_pred_df)))
        
        force_plot = shap.force_plot(explainer.expected_value, shap_values[instance_index, :], new_pred_df.iloc[instance_index, :], matplotlib=True)
        st.pyplot(force_plot)
        if real:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(o_dataframe[" VEL_5_RPM"], o_dataframe["Predictions_VEL_5_RPM"], color='blue')
            ax.plot([o_dataframe[" VEL_5_RPM"].min(), o_dataframe[" VEL_5_RPM"].max()],
                    [o_dataframe[" VEL_5_RPM"].min(), o_dataframe[" VEL_5_RPM"].max()],
                    linestyle='--', color='red')  # Adiciona a linha de referência para comparação
            ax.set_xlabel('Real')
            ax.set_ylabel('Predito')
            ax.set_title('Valores Reais vs. Preditos')
            st.pyplot(fig)
            
            
    if st.session_state['download_pg1_guide3']:
        o_dataframe = st.session_state['dataframe']
        df_xlsx = st.session_state['df_xlsx']
        
        st.write("Click the button to download a new file with the prediction results:")
        st.download_button(label = 'Download',
                                        data = df_xlsx,
                                        file_name = 'prediction_results.csv')
        st.write("Preview:")
        st.write(o_dataframe)

