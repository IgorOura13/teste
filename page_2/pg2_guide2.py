# External libraries
import pandas as pd
import streamlit as st

# Internal libraries
from machine_learning_algorithm import check_data, new_df, train_model

# Dictionaries relating variable's name with its corresponding number

results = {
    0: 'Disapproved',
    1: 'Approved',
}

def run_guide2():
    
    # Tutorial on uploading a csv file

    with st.expander("TUTORIAL"):
        
        st.write('''
            First off, create a new spreadsheet with Google Sheets including your dataset.\n
            Your file must include only the spreadsheet header and rows.
        ''')
        st.markdown("---")
        st.write("Follow the example below, your spreadsheet must match up to this model:")
        st.image("images/tutorial-pg2-foto1.png")
        st.markdown("---")
        st.write("After that, download your CSV file following this example:")
        st.image("images/tutorial-pg2-foto2.png")
        st.markdown("---")
        st.write("Finally, click the 'Browse files' button to upload your file:")
        st.image("images/tutorial-pg2-foto3.png")
        st.markdown("---")
        st.write("That's it! Now you can add new data!")
        

    # Uploading a file

    if 'download_pg2_guide3' not in st.session_state:
            st.session_state['download_pg2_guide3'] = False

    try:

        with st.form("Inputs3"):

            uploaded_file = st.file_uploader("Choose a file:", help = "Please enter a CSV file")
            file = True
            if uploaded_file is not None: 
                added_df = pd.read_csv(uploaded_file, index_col = False)                  
            else:
                file = False
            submitted = st.form_submit_button("Add new data")

            if submitted:
                if file:
                    with st.spinner("Training new model..."):    
                        run_autodeploy = check_data(added_df)
                        if run_autodeploy == True:
                            new_updated_df = new_df(added_df)
                            new_df_csv = new_updated_df.to_csv(index = False).encode('utf-8')
                            new_model = train_model(new_updated_df)

                            if 'new_model_pg2_guide3' not in st.session_state:
                                st.session_state['new_model_pg2_guide3'] = new_model
                            if 'new_df_csv_pg2_guide3' not in st.session_state:
                                st.session_state['new_df_csv_pg2_guide3'] = new_df_csv

                            st.session_state['download_pg2_guide3'] = True
                        else:
                            for error in run_autodeploy[0]:
                                st.error(error)
                            st.warning(run_autodeploy[1])
                            st.image("images/order_of_columns.png")
        
        if st.session_state['download_pg2_guide3']:
            new_model = st.session_state['new_model_pg2_guide3']
            st.download_button(label = 'Download new model',
                                        data = new_model, 
                                        file_name = 'ml_trained_model.sav')

            new_df_csv = st.session_state['new_df_csv_pg2_guide3']
            st.download_button(label = 'Download new data',
                                        data = new_df_csv, 
                                        file_name = 'data.csv')

            st.info("New model and new data must be uploaded to github. Check the tutorial to see how.")
        
        if submitted:
            if not file:      
                st.warning("Warning: no file uploaded")
                
    except (ValueError, UnboundLocalError):
        st.warning("Warning: unable to predict, make sure your file is correct")
