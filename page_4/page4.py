# External library
import streamlit as st

# Internal libraries
from page_4.pg4_guide1 import run_guide1
from page_4.pg4_guide2 import run_guide2

def run_page4():

    with st.expander("Random Forest info"):

        run_guide1()

    with st.expander("Algorithm code"):

        run_guide2()

    st.write(" ")
                    
    st.markdown('<h3 style="text-align:center;">Made by <span style="color:#1A89D3;font-weight:bolder;font-size:30px;"><a style="text-decoration:none;" href="https://www.quanta.org.br/">Quanta Junior</a></span></h3>',unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center;text-decoration:none;font-weight:bolder;"><a style="text-decoration:none;color:#222222;" href="https://github.com/QuantaJunior/unilever">GitHub</a></h3>',unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center;text-decoration:none;font-weight:bolder;"><a style="text-decoration:none;color:#086A99;" href="https://www.quanta.org.br/contato">Contact</a></h3>',unsafe_allow_html=True)
        
    c1, c2, c3 = st.columns([4.8,5,5.1])

    with c1:
        st.write(" ")
                    
    with c2:
        st.image("images/Logo_Quanta.png", use_column_width = 'auto')