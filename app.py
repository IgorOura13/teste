# External libraries
import streamlit as st
from streamlit_option_menu import option_menu

# Internal libraries
from machine_learning_algorithm import dataframe, visc_path, proc_path
from page_1.page1 import run_page1
from page_2.page2 import run_page2
from page_4.page4 import run_page4

# Website's general configurations

st.set_page_config(
     page_icon = "images/Logo.png",
     page_title = "Model's interface",
     layout = "wide",
     initial_sidebar_state = "expanded",
)

st.set_option('deprecation.showPyplotGlobalUse', False)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

hide_streamlit_style2 = """
            <style>
                #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
            </style>
            """
st.markdown(hide_streamlit_style2, unsafe_allow_html=True)

# Username and Password Authentication



# Sidebar
st.sidebar.image("images/unilever-logo.png", use_column_width = 'auto')


if st.sidebar.checkbox("Display data", False):
     st.subheader("Viscosity data:")
     st.write(dataframe(visc_path))
     st.subheader("Processes data:")
     st.write(dataframe(proc_path))

with st.sidebar:
     page = option_menu(
          "Menu", ['Perform a prediction', 'Add new data', 'Informations'], 
          icons = ['box-arrow-right', 'plus-circle', 'info-circle'],
          menu_icon = "house",
          styles = {
               "container": {"padding": "0!important", "background-color": "transparent"},
               #"icon": {"color": "#2962ff"}, 
               "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#a9d4de"},
               "nav-link-selected": {"font-size": "15px", "font-weight": "normal"},
          }
     )

    # Display pages

if page == 'Perform a prediction':

     run_page1()

elif page == 'Add new data':
        
     run_page2()

elif page == 'Informations':

     run_page4()


