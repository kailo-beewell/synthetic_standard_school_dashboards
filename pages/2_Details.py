from ast import literal_eval
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from utilities.fixed_params import page_setup
from utilities.details import details_stacked_bar, details_ordered_bar

# Set page configuration
page_setup('wide')

# Manually set school (will need to change to set globally on login)
school = 'School B'

# Import the scores and the proportion each response
df_scores = pd.read_csv('data/survey_data/aggregate_scores_rag.csv')
df_prop = pd.read_csv('data/survey_data/aggregate_responses.csv')

###############################################################################

# Get the unique topics
topic_df = df_scores[['variable', 'variable_lab']].drop_duplicates()

# Drop those we don't create detailed pages about
topic_df = topic_df[~topic_df['variable'].isin([
    'birth_you_age_score', 'staff_talk_score', 'home_talk_score',
    'peer_talk_score', 'overall_count'])]

# Remove '_score'
topic_df['variable'] = topic_df['variable'].str.replace('_score', '')

# Convert to dictionary
topic_dict = pd.Series(topic_df.variable.values, index=topic_df.variable_lab).to_dict()

# If session state doesn't contain chosen variable, default to Autonomy
# If it does (i.e. set from Summary page), use that
if 'chosen_variable_lab' not in st.session_state:
    st.session_state['chosen_variable_lab'] = 'Autonomy'

# Convert topics to list and find index of the session state variable
topic_list = list(topic_dict.keys())
default = topic_list.index(st.session_state['chosen_variable_lab'])

# Create selectbox with available topics (excluding demographic) using label
chosen_variable_lab = st.sidebar.radio(
    'Topic', topic_dict.keys(), index=default)
chosen_variable = topic_dict[chosen_variable_lab]

###############################################################################
# Breakdown of question responses chart

# Title 
st.title(chosen_variable_lab)

# Introduction
st.markdown(f'''
This page shows you how pupils at your school answered questions relating to the topic of {chosen_variable_lab.lower()}.
You can view answers from all pupils or by year group, gender, free school meals (FSM) or special education needs (SEN). 
An average score for this topic has been calculated and, as on the summary page, you can see how the score compares to other schools.''')

# Blank space
st.markdown('')
st.markdown('')

# Select pupils to view results for
cols = st.columns([0.3, 0.7])
with cols[0]:
    st.selectbox('**View results:**', ['For all pupils', 'By year group', 'By gender', 'By FSM', 'By SEN'])

# Blank space
st.markdown('')
st.markdown('')

st.header('Breakdown of responses from pupils at your school')

# Filter to chosen variable and school
chosen = df_prop[
    (df_prop['group'] == chosen_variable) &
    (df_prop['school_lab'] == school) &
    (df_prop['year_group_lab'] == 'All') &
    (df_prop['gender_lab'] == 'All') &
    (df_prop['fsm_lab'] == 'All') &
    (df_prop['sen_lab'] == 'All')]

# Extract the lists with results stored in the dataframe
# e.g. ['Yes', 'No'], [20, 80], [2, 8] in the original data will become
# seperate columns with [Yes, 20, 2] and [No, 80, 8]
df_list = []
for index, row in chosen.iterrows():
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
    df_list.append(df)
chosen_result = pd.concat(df_list)

# For categories with multiple charts, list the variables for each chart
multiple_charts = {
    'optimism': {'optimism_future': ['optimism_future'],
                 'optimism_other': ['optimism_best', 'optimism_good', 'optimism_work']},
    'appearance': [['appearance_happy'], ['appearance_feel']],
    'physical': [['physical_days'], ['physical_hours']],
    'places': [['places_freq'],
               ['places_barriers___1', 'places_barriers___2',
                'places_barriers___3', 'places_barriers___4',
                'places_barriers___5', 'places_barriers___6',
                'places_barriers___7', 'places_barriers___8',
                'places_barriers___9']],
    'talk': [['staff_talk', 'home_talk', 'peer_talk'],
             ['staff_talk_listen', 'home_talk_listen', 'peer_talk_listen'],
             ['staff_talk_helpful', 'home_talk_helpful', 'peer_talk_helpful'],
             ['staff_talk_if', 'home_talk_if', 'peer_talk_if']],
    'local_env': [['local_safe'],
                  ['local_support', 'local_trust',
                   'local_neighbours', 'local_places']],
    'future': [['future_options'], ['future_interest'], ['future_support']]
}

# EXAMPLE: Description above stacked barchart
stacked_descrip = {
    'autonomy': '''These questions are about how 'in control' young people feel about their lives.  \nPupils were asked how true they felt the following statements to be for themselves.  \nAnswers on the left indicate pupils feel **less** 'in control'  whilst answers on the right indicate pupils feel **more** 'in control'.''',
    'life_satisfaction': '''This question is about how satisfied young people feel with their life.''',
    'home_happy': '''This question is about how happy young people are with the home they live in.  \nYoung people were ask to rate their response on a scale of 0 to 10, where 0 is very unhappy, 5 is neither happy or unhappy, and 10 is very happy''',
    'optimism_future': 'These questions are about how optimistic young people feel about the future.  \nFor all four questions, answers on the left indicate pupils feel **less** optimistic, whilst answers on the right indicate pupils feel **more** optimistic.  \nFor this first question, young people were asked how often they feel optimistic about the future.',
    'optimism_other': 'For these three questions, young people were asked how well they felt the following statements described themselves.'
}

# Create stacked bar chart with seperate charts if required
if chosen_variable in multiple_charts:
    var_dict = multiple_charts[chosen_variable]
    for key, value in var_dict.items():
        # Add description
        st.markdown(stacked_descrip[key])
        # Create plot
        to_plot = chosen_result[chosen_result['measure'].isin(value)]
        details_stacked_bar(to_plot)
# Otherwise create a single stacked bar chart
else:
    if chosen_variable in stacked_descrip:
        st.markdown(stacked_descrip[chosen_variable])
    details_stacked_bar(chosen_result)

###############################################################################
# Blank space
st.text('')
st.text('')
st.text('')

###############################################################################
# Initial basic example of doing the comparator chart between schools...

st.header('Comparison of overall mean score to other schools')

# Create dataframe based on chosen variable
between_schools = df_scores[
    (df_scores['variable'].str.replace('_score', '') == chosen_variable) &
    (df_scores['year_group_lab'] == 'All') &
    (df_scores['gender_lab'] == 'All') &
    (df_scores['fsm_lab'] == 'All') &
    (df_scores['sen_lab'] == 'All')]

# Add box with RAG rating
devon_rag = between_schools.loc[between_schools['school_lab'] == school, 'rag'].to_list()[0]
cols = st.columns(2)
with cols[0]:
    st.subheader('Comparison to other schools in Northern Devon')
    st.markdown(f'The average score for {chosen_variable_lab.lower()} at your school, compared to other schools in Northern Devon, was:')
    if devon_rag == 'below':
        st.error('↓ Below average')
    elif devon_rag == 'average':
        st.warning('~ Average')
    elif devon_rag == 'above':
        st.success('↑ Above average')

# Show figure within column
with cols[1]:
    details_ordered_bar(between_schools, school)

# Note schools that don't have a match (might be able to do that based on
# what variables are present in their data v.s. not)
no_match = ['support', 'places', 'talk', 'accept', 'belong_local', 'wealth', 'future', 'climate']

# Create duplicate to show example of what having matched schools as well looks like
cols = st.columns(2)
if chosen_variable in no_match:
    st.markdown('This question was unique to Northern Devon and cannot be compared to other schools.')
else:
    with cols[0]:
        st.subheader('Comparison to matched schools from across the country')
        st.markdown('Your school:')
        if devon_rag == 'below':
            st.error('↓ Below average')
        elif devon_rag == 'average':
            st.warning('~ Average')
        elif devon_rag == 'above':
            st.success('↑ Above average')
        st.markdown('Note: Just a duplicate of the above')
    with cols[1]:
        details_ordered_bar(between_schools, school)