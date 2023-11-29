import pandas as pd
import streamlit as st
from PIL import Image
from utilities.switch_page_button import switch_page
from utilities.fixed_params import page_setup

# Set page configuration
page_setup('centered')

# Change font size for sidebar
st.markdown('''
<style>
    /* Change text size */
    [data-testid=stSidebarNavItems] {
        font-size: 20px;
    }
</style>
''', unsafe_allow_html=True)

# Centre title
st.markdown('''
<style>
    h1 {
        text-align: center
    }
''', unsafe_allow_html=True)

# Import data used on this page
data = pd.read_csv('data/survey_data/aggregate_scores.csv')

# Manually set school (will need to change to set globally on login)
school = 'School B'

#with open('css/style.css') as css:
#    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)
#st.markdown('''<h1 style='text-align: center;'>School</h1>''', unsafe_allow_html=True)
st.title(school)

st.markdown('''
Thank you for taking part in the #BeeWell survey. This dashboard contains results from pupils at your school, compared with other schools in Northern Devon, and matched schools from across the country.
''')

st.subheader('Guide to the dashboard')
st.markdown('Use the sidebar on the left to navigate to different pages of the dashboard.')

cols = st.columns([0.3, 0.7])
with cols[0]:
    if st.button('Summary'):
        switch_page('summary')
with cols[1]:
    st.markdown('This page gives an overview of how the average results at your school compare with other school, for all pupils and by pupil groups (year group, gender, FSM, SEN).')

cols = st.columns([0.3, 0.7])
with cols[0]:
    if st.button('Details'):
        switch_page('details')
with cols[1]:
    st.markdown('This page provides a breakdown of responses to each question.')

cols = st.columns([0.3, 0.7])
with cols[0]:
    st.info('Pupils')
with cols[1]:
    st.markdown('This page shows the characteristics of pupils who completed the survey at your school, compared with other schools.')

cols = st.columns([0.3, 0.7])
with cols[0]:
    st.info('About')
with cols[1]:
    st.markdown('This page contains background information about the survey.')

st.subheader('FAQs')
with st.expander('How do I use this dashboard?'):
    st.write('Explanation')

with st.expander('How do I print or save a page as a PDF?'):
    st.write('There are several options...')