# External library
import streamlit as st
import pandas as pd

# Internal libraries
from machine_learning_algorithm import new_df, train_model, dataframe

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

def run_guide1():

    # Data input

    try:

        if 'download_pg2_guide1' not in st.session_state:
            st.session_state['download_pg2_guide1'] = False

        with st.form("Inputs1_auto_deploy"):

            var1, var2 = st.columns(2)

            y1 = var1.selectbox("Active:", actives.keys())
            y2 = var2.text_input("Sodium hydroxide:", help = "Unit: %")

            var3, var4 = st.columns(2)

            y3 = var3.text_input("Sodium carbonate:", help = "Unit: %")
            y4 = var4.text_input("Water:", help = "Unit: %")

            var5, var6 = st.columns(2)

            y5 = var5.text_input("Fragance:", help = "Unit: %")
            y6 = var6.text_input("Blue dye:", help = "Unit: %")

            var7, var8 = st.columns(2)

            y7 = var7.text_input("Active percentage:", help = "Unit: %")
            y8 = var8.text_input("Sodium percarbonate:", help = "Unit: %")

            var9, var10 = st.columns(2)

            y9 = var9.selectbox("Test:", tests.keys())
            y10 = var10.text_input("Dosage:", help = "Unit: %")

            var11, var12 = st.columns(2)

            y11 = var11.text_input("Time of contact:", help = "Unit: min")
            y12 = var12.text_input("Temperature:", help = "Unit: ºC")

            y13 = st.selectbox("Final result:", results.values())

            # Corresponding variables with their numbers

            y1 = actives[y1]
            y9 = tests[y9]
            y13 = list(results.keys())[list(results.values()).index(y13)]
            
            def float_values():
                return [float(y) for y in [y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13]]

            submitted = st.form_submit_button("Add new data")

            if submitted:

                with st.spinner("Training new model..."):

                    float_inputs = float_values()
                    columns = list(dataframe().keys())
                    added_df = dict(zip(columns, float_inputs))
                    added_df = pd.DataFrame(added_df, index = [0])
                    new_updated_df = new_df(added_df)
                    new_df_csv = new_updated_df.to_csv(index = False).encode('utf-8')
                    new_model = train_model(new_updated_df)

                    if 'new_model_pg2_guide1' not in st.session_state:
                        st.session_state['new_model_pg2_guide1'] = new_model
                    if 'new_df_csv_pg2_guide1' not in st.session_state:
                        st.session_state['new_df_csv_pg2_guide1'] = new_df_csv
                    st.session_state['download_pg2_guide1'] = True

        if st.session_state['download_pg2_guide1']:
            new_model = st.session_state['new_model_pg2_guide1']
            st.download_button(label = 'Download new model',
                                        data = new_model, 
                                        file_name = 'ml_trained_model.sav')

            new_df_csv = st.session_state['new_df_csv_pg2_guide1']
            st.download_button(label = 'Download new data',
                                        data = new_df_csv, 
                                        file_name = 'data.csv')

            st.info("New model and new data must be uploaded to github. Check the tutorial to see how.")       

    except ValueError:
        st.warning("Warning: please fill in all the gaps")
        st.warning("Warning: please enter numbers only")
