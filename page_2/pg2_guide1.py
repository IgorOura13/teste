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

def run_guide1():

    # Data input

    try:

        if 'download_pg2_guide1' not in st.session_state:
            st.session_state['download_pg2_guide1'] = False

        with st.form("Inputs1_auto_deploy"):
            var1, var2 = st.columns(2)

            y1 = var1.text_input("Corrente Agitador 1601:")
            y2 = var2.text_input("Corrente Agitador 1602:")

            var3, var4 = st.columns(2)

            y3 = var3.text_input("Corrente Agitador 1603:")
            y4 = var4.text_input("Corrente Agitador 1604:")

            var5, var6 = st.columns(2)

            y5 = var5.text_input("Corrente Agitador 1605:")
            y6 = var6.text_input("Corrente BB 1006:")

            var7, var8 = st.columns(2)

            y7 = var7.text_input("Corrente Bomba 1601:")
            y8 = var8.text_input("Corrente Bomba 1602:")

            var9, var10 = st.columns(2)

            y9 = var9.text_input("Potência Agitador 1605:")
            y10 = var10.text_input("Potência Bomba 1006:")

            var11, var12 = st.columns(2)

            y11 = var11.text_input("Vazão Pasta CV:")
            y12 = var12.text_input("Pressão CZ 1603:")

            var13, var14 = st.columns(2)

            y13 = var13.text_input("Pressão CZ 1605:")
            y14 = var14.text_input("Vazão Pasta PV':")

            var15, var16 = st.columns(2)

            y15 = var15.text_input("Temperatura Final:")
            y16 = var16.text_input("Temperatura Holding 1633:")

            var17, var18 = st.columns(2)

            y17 = var17.text_input("Temperatura Holding 1634:")
            y18 = var18.text_input("Temperatura 3 Corpo:")

            var19, var20 = st.columns(2)

            y19 = var19.text_input("Temperatura 1 Corpo:")
            y20 = var20.text_input("Temperatura Amostra:")

            var21, var22 = st.columns(2)

            y21 = var21.text_input("Dosagem Açúcar:")
            y22 = var22.text_input("Dosagem Água:")

            var23, var24 = st.columns(2)

            y23 = var23.text_input("Dosagem Óleo:")
            y24 = var24.text_input("Dosagem Vinagre:")

            y25 = st.selectbox("Final result:", results.values())
            
            submitted = st.form_submit_button("Predict")
            def float_values():
                return [float(y) for y in [y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13, y14, y15, y16, y17, y18, y19, y20, y21, y22, y23, y24]]

            y13 = list(results.keys())[list(results.values()).index(y13)]
            

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
