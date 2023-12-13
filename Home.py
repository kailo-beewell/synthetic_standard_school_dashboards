import pandas as pd
import streamlit as st
from PIL import Image
from utilities.switch_page_button import switch_page
from utilities.fixed_params import page_setup

# Set page configuration
page_setup()

# Import data used on this page
data = pd.read_csv('data/survey_data/aggregate_scores.csv')

###############################################################################

st.title('The #BeeWell Survey')
st.markdown('''<p style='text-align: center;'>This dashboard summarises your schools results from the #BeeWell survey.</p>''', unsafe_allow_html=True)

st.image('images/dashboard_home_section.png', output_format='PNG')

st.subheader('Dashboard guide')
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
    if st.button('Pupils'):
        switch_page('pupils')
with cols[1]:
    st.markdown('This page shows the characteristics of pupils who completed the survey at your school, compared with other schools.')

cols = st.columns([0.3, 0.7])
with cols[0]:
    if st.button('About'):
        switch_page('about')
with cols[1]:
    st.markdown('This page contains background information about the survey.')

st.subheader('FAQs')
with st.expander('Who completed the #BeeWell survey?'):
    st.markdown('''
This year, pupils in Years 8 and 10 at seven secondary schools from across North Devon and Torridge completed the standard version of the #BeeWell survey.
The survey contained questions to measure wellbeing and the factors that might impact it.
#BeeWell surveys were also completed by pupils at schools in Hampshire, Greater Manchester and Havering.
''')
with st.expander('What is the purpose of the survey?'):
    st.markdown('Question answer')
with st.expander('How should we use these results?'):
    st.markdown('Question answer')
with st.expander('Can I access this dashboard on different devices?'):
    st.markdown('''
Yes - although it has been designed to view full screen on a computer/laptop, 
it is possible to view on other devices like a mobile phone. It will resize the 
page to your screen, but if the figures appear cramped/difficult to read, you may want to zoom out.''')

cols = st.columns(3)
with cols[0]:
    st.image('images/discovery-looking-researching.jpg')
with cols[1]:
    st.image('images/levelling-the-ground.jpg')
with cols[2]:
    st.image('images/young-person-journey.jpg')