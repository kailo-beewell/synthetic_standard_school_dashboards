from ast import literal_eval
import numpy as np
import pandas as pd
import streamlit as st
from utilities.fixed_params import page_setup, page_footer
from utilities.details import survey_responses

# Set page configuration
page_setup()

# Import data
df_prop = pd.read_csv('data/survey_data/aggregate_responses.csv')
counts = pd.read_csv('data/survey_data/overall_counts.csv')

###############################################################################
# Introduction including total pupil number

# Title
st.title('Pupils')

# Filter to relevant school
school_counts = counts.loc[counts['school_lab'] == st.session_state.school]

# Find total school size
school_size = school_counts.loc[
    (school_counts['year_group_lab'] == 'All') &
    (school_counts['gender_lab'] == 'All') &
    (school_counts['fsm_lab'] == 'All') &
    (school_counts['sen_lab'] == 'All'), 'count'].values[0].astype(int)

# Print school size
st.markdown(f'''
There were {school_size} pupils at your school who took part in the #BeeWell survey.  
This page describes the sample of pupils who completed the survey.  
''')

st.markdown('''
**To fix:**
* Here it's not about pupil response always and sometimes about whether it was in council data.
* Pupils should say your school rather than All''')

###############################################################################
# Figures

# Select whether to view results alongside other schools or not
chosen_group = st.selectbox(
    '**View results:**', ['For your school',
                          'Compared with other schools in Northern Devon',
                          'Compared with matched schools across the country'])

# SAME AS DETAILS
# Set default values
year_group = ['All']
gender = ['All']
fsm = ['All']
sen = ['All']
group_lab = 'year_group_lab' # set as default group but not used, prevents error

# DIFFERENT TO DETAILS
chosen_variable = 'demographic'

# SAME AS DETAILS
# Filter to chosen variable and school
chosen = df_prop[
    (df_prop['group'] == chosen_variable) &
    (df_prop['school_lab'] == st.session_state.school) &
    (df_prop['year_group_lab'].isin(year_group)) &
    (df_prop['gender_lab'].isin(gender)) &
    (df_prop['fsm_lab'].isin(fsm)) &
    (df_prop['sen_lab'].isin(sen))]

# SAME AS DETAILS
# Extract the lists with results stored in the dataframe
# e.g. ['Yes', 'No'], [20, 80], [2, 8] in the original data will become
# seperate columns with [Yes, 20, 2] and [No, 80, 8]
df_list = []
for index, row in chosen.iterrows():
    # Extract results as long as it isn't NaN (e.g. NaN when n<10)
    if ~np.isnan(row.n_responses):
        df = pd.DataFrame(zip(literal_eval(row['cat'].replace('nan', 'None')),
                            literal_eval(row['cat_lab']),
                            literal_eval(row['percentage']),
                            literal_eval(row['count'])),
                        columns=['cat', 'cat_lab', 'percentage', 'count'])
        # Replace NaN with max number so stays at end of sequence
        df['cat'] = df['cat'].fillna(df['cat'].max()+1)
        # Add measure (don't need to extract as string rather than list in df)
        df['measure'] = row['measure']
        df['measure_lab'] = row['measure_lab']
        df['group'] = row[group_lab]
        df_list.append(df)
    # As we still want a bar when n<10, we create a record still but label as such
    else:
        df = row.to_frame().T[['measure', 'measure_lab']]
        df['group'] = row[group_lab]
        df['cat'] = 0
        df['cat_lab'] = 'Less than 10 responses'
        df['count'] = np.nan
        df['percentage'] = 100
        df_list.append(df)

chosen_result = pd.concat(df_list)

# DIFFERENT TO DETAILS (as no descriptions or reversing)
# Create plot
survey_responses(chosen_result)

page_footer()