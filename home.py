import pandas as pd
import streamlit as st
from PIL import Image
from utilities.switch_page_button import switch_page

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