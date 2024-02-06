# External libraries
import pandas as pd
import streamlit as st

# Internal libraries
from machine_learning_algorithm import check_data, new_df, train_model, tank, model_path, dataframe, visc_path, proc_path
from format_data import run_format_data

# Dictionaries relating variable's name with its corresponding number


def run_guide2():
    
    # Tutorial on uploading a csv file

    with st.expander("TUTORIAL"):
        
        st.write('''
            First off, create a new spreadsheet with Google Sheets including your dataset.\n
            Your file must include only the spreadsheet header and rows.
        ''')
        st.markdown("---")
        st.write("Follow the example below, your spreadsheet must match up to this model for each spreadsheet:")
        st.subheader("Viscosity data example:")
        st.write(dataframe('for_display/display_visc.csv'))
        st.subheader("Processes data example:")
        st.write(dataframe('for_display/display_proc.csv'))
        
        st.markdown("---")
        st.write("After that, download your CSV or xlsx file")
        
        st.markdown("---")
        st.write("Finally, click the 'Browse files' button to upload your file:")
        st.image("images/tutorial-pg2-foto3.png")
        st.markdown("---")
        st.write("That's it! Now you can add new data!")
        

    # Uploading a file

    if 'download_pg2_guide3' not in st.session_state:
            st.session_state['download_pg2_guide3'] = False

    try:
        option_v = st.selectbox('What type of viscosity file?',
            ('CSV', 'Excel'))
        
        option_p = st.selectbox('What type of processes file?',
            ('CSV', 'Excel'))
        with st.form("Inputs3"):
            if option_v == 'CSV':
                uploaded_file_v = st.file_uploader("Upload CSV viscosity spreadsheet:", help = "Please enter a CSV file")
                file = True
                if uploaded_file_v is not None: 
                    added_df_v = pd.read_csv(uploaded_file_v, index_col = False)                  
                else:
                    file = False
            elif option_v == 'Excel':
                uploaded_file_v = st.file_uploader("Upload xlsx viscosity spreadsheet:", help = "Please enter a xlsx file")
                file = True
                if uploaded_file_v is not None: 
                    added_df_v = pd.read_excel(uploaded_file_v, index_col = False)                  
                else:
                    file = False
            if option_p == 'CSV':
                uploaded_file_p = st.file_uploader("Upload processes spreadsheet:", help = "Please enter a CSV file")
                file = True
                if uploaded_file_p is not None: 
                    added_df_p = pd.read_csv(uploaded_file_p, index_col = False)                  
                else:
                    file = False
            elif option_p == 'Excel':
                uploaded_file_p = st.file_uploader("Upload xlsx processes spreadsheet:", help = "Please enter a xlsx file")
                file = True
                if uploaded_file_p is not None: 
                    added_df_p = pd.read_excel(uploaded_file_p, index_col = False)                  
                else:
                    file = False

            submitted = st.form_submit_button("Add data")

            if submitted:
                if file:
                    with st.spinner("Training new model..."):    
                        run_autodeploy = check_data(added_df_v, added_df_p)
                        if run_autodeploy == True:
                            new_updated_df_v = new_df(added_df_v, visc_path)
                            new_updated_df_p = new_df(added_df_p, proc_path)
                            new_updated_df = run_format_data(new_updated_df_p, new_updated_df_v)

                            new_df_csv = new_updated_df.to_csv(index = False).encode('utf-8')
                            new_df_csv_v = new_updated_df_v.to_csv(index = False).encode('utf-8')
                            new_df_csv_p = new_updated_df_p.to_csv(index = False).encode('utf-8')
                            new_updated_df = tank(new_updated_df)
                            new_model = train_model(new_updated_df)

                            if 'new_model_pg2_guide3' not in st.session_state:
                                st.session_state['new_model_pg2_guide3'] = new_model
                            
                            if 'new_df_csvv_pg2_guide3' not in st.session_state:
                                st.session_state['new_df_csvv_pg2_guide3'] = new_df_csv_v
                            if 'new_df_csvp_pg2_guide3' not in st.session_state:
                                st.session_state['new_df_csvp_pg2_guide3'] = new_df_csv_p

                            st.session_state['download_pg2_guide3'] = True
                        else:
                            for error in run_autodeploy[0]:
                                st.error(error)
                            st.warning(run_autodeploy[1])
                            
        
        if st.session_state['download_pg2_guide3']:
            new_model = st.session_state['new_model_pg2_guide3']
            st.download_button(label = 'Download new model',
                                        data = new_model, 
                                        file_name = 'pipeline_model.sav')
            new_df_csv_v = st.session_state['new_df_csvv_pg2_guide3']
            st.download_button(label = 'Download new viscosity data',
                                        data = new_df_csv_v, 
                                        file_name = 'data_visc.csv')
            new_df_csv_p = st.session_state['new_df_csvp_pg2_guide3']
            st.download_button(label = 'Download new processes data',
                                        data = new_df_csv_p, 
                                        file_name = 'data_proc.csv')

            st.info("New model and new data must be uploaded to github. Check the tutorial to see how.")
        
        if submitted:
            if not file:      
                st.warning("Warning: no file uploaded")
                
    except (ValueError, UnboundLocalError):
        st.warning("Warning: unable to predict, make sure your file is correct")
