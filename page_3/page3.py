# External libraries
import streamlit as st
import hydralit_components as hc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from imblearn.over_sampling import RandomOverSampler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_predict, LeaveOneOut
from sklearn.metrics import confusion_matrix, classification_report
import shap
import warnings

# Internal libraries
from machine_learning_algorithm import dataframe, model
from utils import st_shap

def run_page3():

    dashboard_options = [
        {'icon': "bi bi-graph-up", 'label':"Metrics"},
        {'icon':"bi bi-journal-text",'label':"Algorithm Explainer"},
    ]
    over_theme = {'txc_inactive': '#262730','menu_background':'#F0F2F6','txc_active':'white','option_active':'#4073ca'}
    dashboard_option = hc.option_bar(option_definition = dashboard_options,override_theme = over_theme, horizontal_orientation=True, key="page3")

    df = dataframe()

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

    # Differentiating categorical and numerical variables

    Active_column = df.columns[0]
    Test_column = df.columns[8]
    Final_Result_column = df.columns[-1]

    dic = {
    Active_column: 'category',
    Test_column: 'category',
    Final_Result_column: 'category'
    }

    for i in dic.keys():
        df[i] = df[i].astype("category")
    for i in df.keys():
        if i not in dic.keys():
            df[i] = df[i].astype(float, errors = 'raise')

    # Using one-hot-encoding and dividng data between prediction data and answer

    x = df.drop(Final_Result_column, axis = 1) # Prediction data
    x = pd.get_dummies(x) # Using one-hot-encoding to turn categorical variables into binary
    y = df[Final_Result_column] # Real answer

    # Oversampling

    r_over_samp = RandomOverSampler(random_state=0)
    x_resampled, y_resampled = r_over_samp.fit_resample(x, y)

    x_initial = np.array(x_resampled)
    y_initial = np.array(y_resampled)

    try:

        if dashboard_option == "Metrics":

            x, y = x_initial, y_initial

            with st.spinner("Loading dashboard..."):

                # LeaveOneOut Cross Validation

                cv = LeaveOneOut()
                clf = RandomForestClassifier(random_state=42)

                @st.cache(show_spinner = False, ttl = 600)
                def y_pred_cross_val():
                    return cross_val_predict(clf, x, y, cv=cv, n_jobs=-1)
                y_pred = y_pred_cross_val()

                report_dic = classification_report(y, y_pred, digits=4, output_dict = True)

                col1, col2, col3, col4, col5 = st.columns(5)

                with col1:
                    value1 = round(report_dic["macro avg"]["precision"]*100, 2)
                    st.write("")
                    st.write("")
                    st.write("Precision Average:")
                    st.info(f"{value1} %")

                with col2:
                    value2 = round(report_dic["macro avg"]["recall"]*100, 2)
                    st.write("")
                    st.write("")
                    st.write("Recall Average:")
                    st.info(f"{value2} %")

                with col3:
                    st.write("Classes:")
                    st.error("Disapproved:")
                    st.success("Approved:")

                with col4:
                    value3 = round(report_dic["0"]["precision"]*100, 2)
                    value4 = round(report_dic["1"]["precision"]*100, 2)
                    st.write("Precision:")
                    st.info(f"{value3} %")
                    st.info(f"{value4} %")

                with col5:
                    value5 = round(report_dic["0"]["recall"]*100, 2)
                    value6 = round(report_dic["1"]["recall"]*100, 2)
                    st.write("Recall:")
                    st.info(f"{value5} %")
                    st.info(f"{value6} %")

                st.write("---")

                # Get and reshape confusion matrix data
                matrix = confusion_matrix(y, y_pred)
                matrix = matrix.astype('float') / matrix.sum(axis=1)[:, np.newaxis]

                # Build the plot
                fig_1 = plt.figure(figsize=(16,7))
                sns.set(font_scale=1.4)
                sns.heatmap(matrix, annot=True, annot_kws={'size':10},
                            cmap="Blues", linewidths=0.2)

                # Add labels to the plot
                class_names = ['Disapproved', 'Approved']
                tick_marks = np.arange(len(class_names))
                tick_marks2 = tick_marks + 0.5
                plt.xticks(tick_marks, class_names, ha='left', rotation=0)
                plt.yticks(tick_marks2, class_names, rotation=0)
                plt.xlabel('Predicted label', labelpad=25, ha='center')
                plt.ylabel('True label', labelpad=25)
                plt.title('Confusion Matrix for Random Forest Model')
                st.pyplot(fig_1, width=16,height=7)

                st.write("")
                st.write("---")

                co1, co2, co3 = st.columns([0.85,5,0.85])

                data_mask = df[Final_Result_column] == 1
                filter_df1 = df[data_mask]
                data_mask2 = df[Final_Result_column] == 0
                filter_df2 = df[data_mask2]

                with co2:

                    correlation1 = filter_df1.corr()
                    fig_2 = plt.figure(figsize = (13,10))
                    sns.set(font_scale=1)
                    sns.heatmap(correlation1, annot = True, fmt=".1f", linewidths=.5, cmap = 'RdBu', vmin = -1, vmax = 1)
                    plt.xticks(rotation=50, ha='right', rotation_mode="anchor")
                    plt.title('Correlation Matrix Between Features for Approved Data', fontsize = 20)
                    st.pyplot(fig_2, width=13,height=10)

                st.write("---")

                co3, co4, co5 = st.columns([0.85,5,0.85])

                with co4:

                    correlation2 = filter_df2.corr()
                    fig_3 = plt.figure(figsize = (13,10))
                    sns.set(font_scale=1)
                    sns.heatmap(correlation2, annot = True, fmt=".1f", linewidths=.5, cmap = 'RdBu', vmin = -1, vmax = 1)
                    plt.xticks(rotation=50, ha='right', rotation_mode="anchor")
                    plt.title('Correlation Matrix Between Features for Disapproved Data', fontsize = 20)
                    st.pyplot(fig_3, width=13,height=10)

        elif dashboard_option == "Algorithm Explainer":

            x, y = x_initial, y_initial

            with st.spinner("Loading dashboard..."):

                warnings.filterwarnings("ignore")
                clf = model()
                
                # SHAP

                x = x_resampled
                explainer = shap.TreeExplainer(clf)
                shap_values = explainer.shap_values(x)
                x.columns = ind

                st_shap(shap.force_plot(explainer.expected_value[1], shap_values[1], x), height = 400)

                st.write("---")

                col1, col2, col3 = st.columns([10,2,10])

                with col1:
                    
                    fig_4 = shap.summary_plot(shap_values[1], x)
                    st.pyplot(fig_4, width=1440,height=288)

                with col3:                    

                    option1 = st.selectbox("First Feature", ind)
                    option2 = st.selectbox("Interaction Feature", [None]+ind)

                    st.write("")

                    fig_5 = shap.dependence_plot(option1, shap_values[1], x, interaction_index=option2)
                    st.pyplot(fig_5, width=1440,height=288)

                st.write("")

                clf.fit(x, y)
                feat_import = pd.Series(clf.feature_importances_)
                feat_import.index = ind
                feat_import_growing = feat_import.sort_values()

                fig_6 = plt.figure(figsize = (13,6))
                sns.barplot(x=feat_import.keys(), y=feat_import, palette = "Blues_d", order=feat_import_growing.keys())
                plt.xlabel('Feature', labelpad=25, fontsize = 15)
                plt.title('Feature Importance', fontsize = 15)
                plt.ylabel('Importance', labelpad=25, fontsize = 15)
                plt.tick_params(labelsize=8)
                plt.xticks(fontsize = 8, rotation=50, ha='right', rotation_mode="anchor")
                st.pyplot(fig_6, width=13,height=6)

    except UnboundLocalError:
        pass