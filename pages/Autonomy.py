from ast import literal_eval
import math
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from utilities.fixed_params import page_setup

# Set page configuration
page_setup('wide')

# Need to change to globally set school depending on login
school = st.selectbox(
    'School', ['School A', 'School B', 'School C', 'School D',
               'School E', 'School F', 'School G'])


st.title('''Autonomy''')

# Import the scores and the proportion each response
df_scores = pd.read_csv('data/survey_data/aggregate_scores_rag.csv')
df_prop = pd.read_csv('data/survey_data/aggregate_responses.csv')

# Test run - but need to change to a smarter way
# Won't actually want to toggle change on page as seperate pages for each
# measure so can customise the page (as some will display multiple seperate graphs)
chosen_variable = st.selectbox(
    'Chosen variable',
    ['Autonomy', 'Stress and coping'])
constituents = {
    'Autonomy': ['autonomy_pressure', 'autonomy_express', 'autonomy_decide',
                 'autonomy_told', 'autonomy_myself', 'autonomy_choice'],
    'Stress and coping': ['stress_control', 'stress_overcome',
               'stress_confident', 'stress_way']
}

# Testing out labels (would need to move to csv creation rather than here)
labels = {
    'autonomy_pressure': 'I feel pressured in my life',
    'autonomy_express': 'I generally feel free to express my ideas and opinions',
    'autonomy_decide': 'I feel like I am free to decide for myself how to live my life',
    'autonomy_told': 'In my daily life I often have to do what I am told',
    'autonomy_myself': 'I feel I can pretty much be myself in daily situations',
    'stress_control': 'In the last month, how often have you felt that you were unable to control the important things in your life?',
    'stress_overcome': 'In the last month, how often have you felt difficulties were piling up so high that you could not overcome them?',
    'stress_confident': 'In the last month, how often have you felt confident about your ability to handle your personal problems?',
    'stress_way': 'In the last month, how often have you felt that things were going your way?'
}
df_prop['measure_lab'] = df_prop['measure'].map(labels)

st.header('Breakdown of responses for your school')

# Filter to chosen variable and school
chosen = df_prop[
    (df_prop['measure'].isin(constituents[chosen_variable])) &
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
    df = pd.DataFrame(zip(literal_eval(row['cat_lab']),
                          literal_eval(row['percentage']),
                          literal_eval(row['count'])),
                      columns=['cat_lab', 'percentage', 'count'])
    df['measure_lab'] = row['measure_lab']
    df_list.append(df)
chosen_result = pd.concat(df_list)

# Create plot, and add percent sign to the numbers labelling the bars
fig = px.bar(
    chosen_result, x='percentage', y='measure_lab', color='cat_lab',
    text_auto=True, title=chosen_variable, hover_data=['count'],
    orientation='h').for_each_trace(
        lambda t: t.update(texttemplate = t.texttemplate + ' %'))

# Disable zooming and panning
fig.layout.xaxis.fixedrange = True
fig.layout.yaxis.fixedrange = True

# Show plot
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

###############################################################################
# Initial basic example of doing the comparator chart between schools...

# Set up columns
cols = st.columns(2)

# Print text about the school in first column
with cols[0]:
    st.header('Comparison to other schools in Northern Devon')
    st.markdown('Your school was below average / average / above average')

# Create dataframe based on chosen variable
between_schools = df_scores[
    (df_scores['variable_lab'] == chosen_variable) &
    (df_scores['year_group_lab'] == 'All') &
    (df_scores['gender_lab'] == 'All') &
    (df_scores['fsm_lab'] == 'All') &
    (df_scores['sen_lab'] == 'All')]

# Add colour for bar based on school
between_schools['colour'] = np.where(
    between_schools['school_lab']==school, '#004E7C', '#6699CC')

# Plot the results
fig = px.bar(between_schools, x='school_lab', y='mean',
             color='colour', color_discrete_map='identity')

# Reorder x axis so in ascending order
fig.update_layout(xaxis={'categoryorder':'total ascending'})

# Set y axis limits to nearest int above and below the min and max
ymin = math.floor(between_schools['mean'].min())
ymax = math.ceil(between_schools['mean'].max())
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