# External library
import streamlit as st
import pandas as pd
import shap
import warnings

# Internal library
from machine_learning_algorithm import model, dataframe, predict
from utils import st_shap

# Dictionaries relating variables' names with their corresponding numbers

results = {
    0: 'Disapproved',
    1: 'Approved',
}

# Columns names for plots

proc = ['Corrente Agitador 1601',
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
visc = []

def run_guide1():

    # Data input

    try:

        if 'predict_pg1_guide1' not in st.session_state:
            st.session_state['predict_pg1_guide1'] = False

        with st.form("Inputs1"):

            var1, var2 = st.columns(2)

            x1 = var1.text_input("Corrente Agitador 1601:")
            x2 = var2.text_input("Corrente Agitador 1602:")

            var3, var4 = st.columns(2)

            x3 = var3.text_input("Corrente Agitador 1603:")
            x4 = var4.text_input("Corrente Agitador 1604:")

            var5, var6 = st.columns(2)

            x5 = var5.text_input("Corrente Agitador 1605:")
            x6 = var6.text_input("Corrente BB 1006:")

            var7, var8 = st.columns(2)

            x7 = var7.text_input("Corrente Bomba 1601:")
            x8 = var8.text_input("Corrente Bomba 1602:")

            var9, var10 = st.columns(2)

            x9 = var9.text_input("Potência Agitador 1605:")
            x10 = var10.text_input("Potência Bomba 1006:")

            var11, var12 = st.columns(2)

            x11 = var11.text_input("Vazão Pasta CV:")
            x12 = var12.text_input("Pressão CZ 1603:")

            var13, var14 = st.columns(2)

            x13 = var13.text_input("Pressão CZ 1605:")
            x14 = var14.text_input("Vazão Pasta PV':")

            var15, var16 = st.columns(2)

            x15 = var15.text_input("Temperatura Final:")
            x16 = var16.text_input("Temperatura Holding 1633:")

            var17, var18 = st.columns(2)

            x17 = var17.text_input("Temperatura Holding 1634:")
            x18 = var18.text_input("Temperatura 3 Corpo:")

            var19, var20 = st.columns(2)

            x19 = var19.text_input("Temperatura 1 Corpo:")
            x20 = var20.text_input("Temperatura Amostra:")

            var21, var22 = st.columns(2)

            x21 = var21.text_input("Dosagem Açúcar:")
            x22 = var22.text_input("Dosagem Água:")

            var23, var24 = st.columns(2)

            x23 = var23.text_input("Dosagem Óleo:")
            x24 = var24.text_input("Dosagem Vinagre:")
            
            submitted = st.form_submit_button("Predict")
            def float_values():
                return [float(x) for x in [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, x19, x20, x21, x22, x23, x24]]


            if submitted:

                float_inputs = float_values()
                columns = list(dataframe().keys())
                prediction_df = dict(zip(columns, float_inputs))
                prediction_df = pd.DataFrame(prediction_df, index = [0])
                prediction_df = predict(prediction_df)

                clf = model()
                float_prediction = clf.predict(prediction_df)
                prediction = results[float_prediction[0]]

                if prediction == 'Disapproved':
                    st.error(prediction)
                elif prediction == 'Approved':
                    st.success(prediction)

                st.session_state['predict_pg1_guide1'] = True

        if st.session_state['predict_pg1_guide1']:

            # Explainer algorithm

            warnings.filterwarnings("ignore")

            st.write("Variables influence in decision classification:")

            explainer = shap.TreeExplainer(clf)
            shap_values = explainer.shap_values(prediction_df)

    except ValueError:
        st.warning("Warning: please fill in all the gaps")
        st.warning("Warning: please enter numbers only")


            
          
