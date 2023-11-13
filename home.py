import pandas as pd
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='#BeeWell School Dashboard',
    page_icon='🐝',
    initial_sidebar_state='expanded'
)

data = pd.read_csv('data/survey_data/aggregate_scores.csv')
illustration = Image.open('images/levelling-the-ground.jpg')

# Need to change to globally set school depending on login
school = st.radio('School', ['School A', 'School B', 'School C', 'School D',
                             'School E', 'School F', 'School G'])

# Need to move this into a functions section
def switch_page(page_name: str):
    '''
    Switch page programmatically in a multipage app
    Copied from streamlit_extras: https://github.com/arnaudmiribel/streamlit-extras

    Args:
        page_name (str): Target page name
    '''
    from streamlit.runtime.scriptrunner import RerunData, RerunException
    from streamlit.source_util import get_pages

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")

    page_name = standardize_name(page_name)

    pages = get_pages('home.py')

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise RerunException(
                RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")


st.title(school)

# Need to move this into a text section
st.markdown('Thank for taking part in the #BeeWell survey. At your school, n pupils completed the survey.')
st.markdown('''
Your survey results are provided, including comparison against:
* Other schools in Northern Devon
* Matched schools from across the country (based on having similar ethnicity, FSM, size and rurality)
Use the sidebar or the buttons below…
''')

if st.button('View survey results'):
    switch_page('summary')

if st.button('Characteristics of pupils who took the survey'):
    switch_page('pupils')

if st.button('About the survey'):
    switch_page('about')

st.image(illustration)