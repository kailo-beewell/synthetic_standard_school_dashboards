import pandas as pd
import streamlit as st
from utilities.fixed_params import page_setup

# Set page configuration
page_setup()

st.title('Pupils')

# Import data and images used on this page
data = pd.read_csv('data/survey_data/aggregate_scores.csv')

# Manually set school (will need to change to set globally on login)
school = 'School B'

# Find school size
school_size = data.loc[
    (data['school_lab'] == school) &
    (data['variable'] == 'overall_count') &
    (data['year_group_lab'] == 'All') &
    (data['gender_lab'] == 'All') &
    (data['fsm_lab'] == 'All') &
    (data['sen_lab'] == 'All'), 'count'].values[0].astype(int)

st.markdown(f'At your school, {school_size} pupils completed the survey.')