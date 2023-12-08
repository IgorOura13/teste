# External library
import streamlit as st
import pandas as pd
import shap
import warnings

# Internal library
from machine_learning_algorithm import model, dataframe
from utils import one_hot_for_prediction, st_shap

# Dictionaries relating variables' names with their corresponding numbers

results = {
    0: 'Disapproved',
    1: 'Approved',
}

actives = {
    'None': 0,
    'Sodium Alkyl Benzene Sulfonate': 1,
    'Benzalkonium Chloride': 2,
    'Dialkyloxyethyl Hydroxyethyl Methyl Ammonium Methyl Sulphate': 3,
    'Hydrogen Peroxide': 4,
    'Sodium hypochlorite': 5,
    'Ethoxylated Alcohol': 6,
    'Lactic acid': 7,
    'Alkyl Dimethyl Benzyl Ammonium Chloride': 8
}

tests = {
    'EN1276': 1,
    'ASTM2274': 2,
    'EN1040': 3,
    'Inhibition halo': 4,
    'OECD202': 5,
    'EN13697': 6,
    'EN14561': 7
}

# Columns names for plots

ind = ['Sodium_hydroxide',
    'Sodium_carbonate',
    'Water',
    'Fragance',
    'Blue_dye',
    'Active_percentage',
    'Sodium_percabonate',
    'Dosage',
    'Time_of_contact',
    'Temperature',
    'No_active',
    'Sodium_Alkyl_Benzene_Sulfonate',
    'Benzalkonium_Chloride',
    'Dialkyloxyethyl_Hydroxyethyl',
    'Hydrogen_Peroxide',
    'Sodium_hypochlorite',
    'Ethoxylated_Alcohol',
    'Lactic_acid',
    "Alkyl_Dimethyl_Benzyl",
    'EN1276',
    'ASTM2274',
    'EN1040',
    'Inhibition halo',
    'OECD202',
    'EN13697',
    'EN14561']

def run_guide1():

    # Data input

    try:

        if 'predict_pg1_guide1' not in st.session_state:
            st.session_state['predict_pg1_guide1'] = False
        
        with st.form("Inputs1"):

            var1, var2 = st.columns(2)

            x1 = var1.selectbox("Active:", actives.keys())
            x2 = var2.text_input("Sodium hydroxide:", help = "Unit: %")

            var3, var4 = st.columns(2)

            x3 = var3.text_input("Sodium carbonate:", help = "Unit: %")
            x4 = var4.text_input("Water:", help = "Unit: %")

            var5, var6 = st.columns(2)

            x5 = var5.text_input("Fragance:", help = "Unit: %")
            x6 = var6.text_input("Blue dye:", help = "Unit: %")

            var7, var8 = st.columns(2)

            x7 = var7.text_input("Active percentage:", help = "Unit: %")
            x8 = var8.text_input("Sodium percarbonate:", help = "Unit: %")

            var9, var10 = st.columns(2)

            x9 = var9.selectbox("Test:", tests.keys())
            x10 = var10.text_input("Dosage:", help = "Unit: %")

            var11, var12 = st.columns(2)

            x11 = var11.text_input("Time of contact:", help = "Unit: min")
            x12 = var12.text_input("Temperature:", help = "Unit: ºC")

            # Corresponding variables with their numbers

            x1 = actives[x1]
            x9 = tests[x9]
            
            def float_values():
                return [float(x) for x in [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12]]

            submitted = st.form_submit_button("Predict")
            
            if submitted:

                float_inputs = float_values()
                columns = list(dataframe().keys())
                prediction_df = dict(zip(columns, float_inputs))
                prediction_df = pd.DataFrame(prediction_df, index = [0])
                prediction_df = one_hot_for_prediction(prediction_df)

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

            prediction_df.columns = ind

            if prediction == 'Disapproved':
                st_shap(shap.force_plot(explainer.expected_value[0], shap_values[1][0,:], prediction_df.iloc[0,:]), height = 150)
            elif prediction == 'Approved':
                st_shap(shap.force_plot(explainer.expected_value[1], shap_values[1][0,:], prediction_df.iloc[0,:]), height = 150)

    except ValueError:
        st.warning("Warning: please fill in all the gaps")
        st.warning("Warning: please enter numbers only")
