# External libraries
import hydralit_components as hc

# Internal libraries
from page_1.pg1_guide1 import run_guide1
from page_1.pg1_guide2 import run_guide2

def run_page1():

    try:

        guides = [
            {'icon': "bi bi-pencil-square", 'label':"Add data by hand"},
            {'icon':"bi bi-file-earmark-arrow-up",'label':"Upload spreadsheet"},
        ]
        over_theme = {'txc_inactive': '#262730','menu_background':'#F0F2F6','txc_active':'white','option_active':'#4073ca'}
        guide = hc.option_bar(option_definition = guides,override_theme = over_theme, horizontal_orientation=True, key="page1")

        if guide == "Add data by hand":

            run_guide1()

        elif guide == "Upload spreadsheet":

            run_guide2()
    
    except UnboundLocalError:
        pass