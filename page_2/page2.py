# External libraries
import hydralit_components as hc

# Internal libraries
from page_2.pg2_guide1 import run_guide1
from page_2.pg2_guide2 import run_guide2

def run_page2():

    guides_auto = [
            {'icon': "bi bi-pencil-square", 'label':"Add data by hand"},
            {'icon':"bi bi-file-earmark-arrow-up",'label':"Upload spreadsheet"},
        ]    
    over_theme_auto = {'txc_inactive': '#262730','menu_background':'#F0F2F6','txc_active':'white','option_active':'#4073ca'}
    guide_auto = hc.option_bar(option_definition = guides_auto,override_theme = over_theme_auto, horizontal_orientation=True, key="page2")

    if guide_auto == "Add data by hand":

        run_guide1()

    elif guide_auto == "Upload spreadsheet":

        run_guide2()