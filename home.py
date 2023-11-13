import pandas as pd
import streamlit as st
from PIL import Image
from utilities.switch_page_button import switch_page
from utilities.fixed_params import page_setup

# Set page configuration
page_setup()

# Import data and images used on this page
data = pd.read_csv('data/survey_data/aggregate_scores.csv')
illustration = Image.open('images/levelling-the-ground.jpg')

# Need to change to globally set school depending on login
school_name = st.radio('School', ['School A', 'School B', 'School C', 'School D',
                             'School E', 'School F', 'School G'])

# Find school size
school_size = data.loc[
    (data['school_lab'] == school_name) &
    (data['variable'] == 'overall_count') &
    (data['year_group_lab'] == 'All') &
    (data['gender_lab'] == 'All') &
    (data['fsm_lab'] == 'All') &
    (data['sen_lab'] == 'All'), 'count'].values[0].astype(int)

st.title(school_name)

# Need to move this into a text section
st.markdown(f'Thank for taking part in the #BeeWell survey. At your school, {school_size} pupils completed the survey.')
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