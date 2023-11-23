from ast import literal_eval
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from utilities.fixed_params import page_setup
from utilities.details import details_stacked_bar

# Set page configuration
page_setup('wide')

# Need to change to globally set school depending on login
school = st.selectbox(
    'School', ['School A', 'School B', 'School C', 'School D',
               'School E', 'School F', 'School G'])

# Import the scores and the proportion each response
df_scores = pd.read_csv('data/survey_data/aggregate_scores_rag.csv')
df_prop = pd.read_csv('data/survey_data/aggregate_responses.csv')

###############################################################################
# Breakdown of question responses chart
# Basic example
# TO DO: how deal with multiple questions with different responses categories

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

# Create selectbox with available topics (excluding demographic) using label
chosen_variable_lab = st.sidebar.radio('Topic', topic_dict.keys())
chosen_variable = topic_dict[chosen_variable_lab]

# Title and header
st.title(chosen_variable_lab)
st.header('Breakdown of responses for your school')

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

multiple_charts = {
    'optimism': [['optimism_future'],
                 ['optimism_best', 'optimism_good', 'optimism_work']],
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

# Create stacked bar chart - with seperate charts if required
if chosen_variable in multiple_charts:
    var_list = multiple_charts[chosen_variable]
    for var in var_list:
        to_plot = chosen_result[chosen_result['measure'].isin(var)]
        details_stacked_bar(to_plot)
else:
    details_stacked_bar(chosen_result)

###############################################################################
# Initial basic example of doing the comparator chart between schools...

# Set up columns
cols = st.columns(2)

# Create dataframe based on chosen variable
between_schools = df_scores[
    (df_scores['variable'].str.replace('_score', '') == chosen_variable) &
    (df_scores['year_group_lab'] == 'All') &
    (df_scores['gender_lab'] == 'All') &
    (df_scores['fsm_lab'] == 'All') &
    (df_scores['sen_lab'] == 'All')]

# Add box with RAG rating
devon_rag = between_schools.loc[between_schools['school_lab'] == school, 'rag'].to_list()[0]
with cols[0]:
    st.header('Comparison to other schools in Northern Devon')
    if devon_rag == 'below':
        st.error('↓ Below average')
    elif devon_rag == 'average':
        st.warning('~ Average')
    elif devon_rag == 'above':
        st.success('↑ Above average')

# Add colour for bar based on school
between_schools['colour'] = np.where(
    between_schools['school_lab']==school, '#2A52BE', '#9BAEE0')

# Plot the results
fig = px.bar(between_schools, x='school_lab', y='mean',
             color='colour', color_discrete_map='identity')

# Reorder x axis so in ascending order
fig.update_layout(xaxis={'categoryorder':'total ascending'})

# Set y axis limits so the first and last bars of the chart a consistent height
# between different plots - find 15% of range and adj min and max by that
min = between_schools['mean'].min()
max = between_schools['mean'].max()
adj_axis = (max - min)*0.15
ymin = min - adj_axis
ymax = max + adj_axis
fig.update_layout(yaxis_range=[ymin, ymax])

# Extract lower and upper rag boundaries amd shade the RAG areas
# (Colours used were matched to those from the summary page)
lower = between_schools['lower'].to_list()[0]
upper = between_schools['upper'].to_list()[0]
fig.add_hrect(y0=ymin, y1=lower, fillcolor='#F8DCDC', layer='below',
              line={'color': '#9A505B'}, line_width=0.5,
              annotation_text='Below average', annotation_position='top left')
fig.add_hrect(y0=lower, y1=upper, fillcolor='#F8ECD4', layer='below',
              line={'color': '#B3852A'}, line_width=0.5,
              annotation_text='Average', annotation_position='top left')
fig.add_hrect(y0=upper, y1=ymax, fillcolor='#E0ECDC', layer='below',
              line={'color': '#3A8461'}, line_width=0.5,
              annotation_text='Above average', annotation_position='top left')

# Prevent zooming and panning, remove grid, and hide plotly toolbar
fig.layout.xaxis.fixedrange = True
fig.layout.yaxis.fixedrange = True
fig.update_yaxes(showgrid=False)

# Show figure within column
with cols[1]:
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})