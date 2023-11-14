import pandas as pd
import streamlit as st
from utilities.fixed_params import page_setup

# Set page configuration
page_setup()

# Need to change to globally set school depending on login
school = st.selectbox(
    'School', ['School A', 'School B', 'School C', 'School D',
               'School E', 'School F', 'School G'])

st.title('''Your school's results''')

##########################################################

# METHOD 1: Dataframes

# Import data
data = pd.read_csv('data/survey_data/aggregate_scores_rag.csv')

# Choose what to show
chosen_group = st.selectbox('Results:', ['All pupils', 'By year group', 'By gender', 'By FSM', 'By SEN'])
comparator = st.selectbox('Compared against:', ['Other schools in Northern Devon'])

# Filter data depending on choice
year_group = ['All']
gender = ['All']
fsm = ['All']
sen = ['All']
if chosen_group == 'By year group':
    pivot_var = 'year_group_lab'
    year_group = ['8.0', '10.0']
elif chosen_group == 'By gender':
    pivot_var = 'gender_lab'
    gender = ['Boy', 'Currently unsure', 'Girl',
              'I describe myself in another way', 'Non-binary',
              'Prefer not to say']
elif chosen_group == 'By FSM':
    pivot_var = 'fsm_lab'
    fsm = ['Yes', 'No']
elif chosen_group == 'By SEN':
    pivot_var = 'sen_lab'
    sen = ['Yes', 'No']

# Filter data
chosen = data[
    (data['school_lab'] == school) &
    (data['year_group_lab'].isin(year_group)) &
    (data['gender_lab'].isin(gender)) &
    (data['fsm_lab'].isin(fsm)) &
    (data['sen_lab'].isin(sen)) &
    (~data['variable'].isin(['birth_you_age_score', 'overall_count']))]

# ISSUE: This reorders the columns
if chosen_group != 'All pupils':
    chosen = chosen[['variable', pivot_var, 'rag']].pivot(
        index='variable', columns=pivot_var, values='rag').reset_index()
else:
    chosen = chosen[['variable', 'rag']]

# Introduce
st.markdown('Click on a row to see results from that topic in more detail...')

# Show dataframe
st.dataframe(chosen, use_container_width=True, hide_index=True)

##########################################################

st.markdown('Click on a row to see results from that topic in more detail...')

# Set number of columns
ncol = len(chosen.columns)

# Add column names
cols = st.columns(ncol)
for i in range(ncol):
    with cols[i]:
        st.markdown('**' + chosen.columns[i] + '**')

# For each row of dataframe, create streamlit columns and write data from cell
for index, row in chosen.iterrows():
    cols = st.columns(ncol)
    for i in range(ncol):
        with cols[i]:
            st.markdown(row[i])

# METHOD 2: Columns
# Can't have one button at end of each as they need unique labels
col1, col2, col3 = st.columns([0.4, 0.2, 0.4])
with col1:
    st.markdown('**Topic**')
with col2:
    st.markdown('**All pupils**')

col1, col2, col3 = st.columns([0.4, 0.2, 0.4])
with col1:
    st.markdown('**Autonomy**', help='''Autonomy is about how 'in control' students feel about their lives''')
with col2:
    st.markdown('✅')

col1, col2, col3 = st.columns([0.4, 0.2, 0.4])
with col1:
    st.markdown('**Life satisfaction**', help='''Life satisfaction is about how satisfied students feel with their lives''')
with col2:
    st.markdown('❗')

with st.expander('Autonomy'):
    st.write('You can see more')