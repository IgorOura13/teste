# External library
import streamlit as st

# Random Forest Text

def run_guide1():

    st.info('''
    Random forests or random decision forests is an ensemble learning method for classification, regression
    and other tasks that operates by constructing a multitude of decision trees at training time.
    \n
    For classification tasks, the output of the random forest is the class selected by most trees. For
    regression tasks, the mean or average prediction of the individual trees is returned.
    \n
    Based on that, we built a Random Forest algorithm to predict whether a substance is a Disinfectant/Sanitizer
    (Approved) or not (Disapproved).
    ''')