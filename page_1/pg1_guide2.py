# External libraries
import pandas as pd
import streamlit as st
import shap
import warnings

# Internal libraries
from machine_learning_algorithm import model
from utils import to_excel, one_hot_for_prediction, st_shap

# Dictionaries relating variable's name with its corresponding number

results = {
    0: 'Disapproved',
    1: 'Approved',
}

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
        st.write("Follow the example below, your spreadsheet must match up to this model:")
        st.image("images/tutorial-pg1-foto1.png")
        st.markdown("---")
        st.write("After that, download your CSV file following this example:")
        st.image("images/tutorial-pg1-foto2.png")
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

        with st.form("Inputs3"):

            uploaded_file = st.file_uploader("Choose a file:", help = "Please enter a CSV file")
            file = True
            if uploaded_file is not None: 
                dataframe = pd.read_csv(uploaded_file, index_col = False)                  
                prediction_df = one_hot_for_prediction(dataframe)
            else:
                file = False
            submitted = st.form_submit_button("Predict")

            if submitted:
                if file:     
                    clf = model()
                    float_prediction = clf.predict(prediction_df)

                    for el in float_prediction:
                        prediction = results[el]
                        if prediction == 'Disapproved':
                            st.error(prediction)
                        elif prediction == 'Approved':
                            st.success(prediction)

                    dataframe['Final_Result'] = float_prediction
                    df_xlsx = to_excel(dataframe)

                    if 'dataframe' not in st.session_state:
                        st.session_state['dataframe'] = dataframe
                    if 'df_xlsx' not in st.session_state:
                        st.session_state['df_xlsx'] = df_xlsx
                    if 'prediction_df' not in st.session_state:
                        st.session_state['prediction_df'] = prediction_df
                    if 'float_prediction' not in st.session_state:
                        st.session_state['float_prediction'] = float_prediction
                    if 'clf' not in st.session_state:
                        st.session_state['clf'] = clf

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
        clf = st.session_state['clf']

        dic_predictions = {}
        for el in range(len(prediction_df)):
            name = f"Prediction {el+1}"
            dic_predictions[name] = (prediction_df.iloc[[el]], float_prediction[el])

        option = st.selectbox("Choose a prediction:", dic_predictions.keys())

        prediction_df_aux = dic_predictions[option][0]
        prediction_aux = dic_predictions[option][1]
        explainer = shap.TreeExplainer(clf)
        shap_values = explainer.shap_values(prediction_df_aux)

        prediction_df_aux.columns = ind

        if prediction_aux == 0:
            st_shap(shap.force_plot(explainer.expected_value[0], shap_values[1][0,:], prediction_df_aux.iloc[0,:]), height = 150)
        elif prediction_aux == 1:
            st_shap(shap.force_plot(explainer.expected_value[1], shap_values[1][0,:], prediction_df_aux.iloc[0,:]), height = 150)

    if st.session_state['download_pg1_guide3']:
        dataframe = st.session_state['dataframe']
        df_xlsx = st.session_state['df_xlsx']

        st.write("Click the button to download a new file with the prediction results:")
        st.download_button(label = 'Download',
                                        data = df_xlsx,
                                        file_name = 'prediction_results.xlsx')
        st.write("Preview:")
        st.write(dataframe)
