from ast import literal_eval
import pandas as pd
import plotly.express as px
import streamlit as st
from utilities.fixed_params import page_setup

# Set page configuration
page_setup()

# Need to change to globally set school depending on login
school = st.selectbox(
    'School', ['School A', 'School B', 'School C', 'School D',
               'School E', 'School F', 'School G'])


st.title('''Autonomy''')

data = pd.read_csv('data/survey_data/aggregate_responses.csv')

# Test run - but need to change to a smarter way
# Won't actually want to toggle change on page as seperate pages for each
# measure so can customise the page (as some will display multiple seperate graphs)
chosen_variable = st.selectbox(
    'Chosen variable',
    ['Autonomy', 'Stress'])
constituents = {
    'Autonomy': ['autonomy_pressure', 'autonomy_express', 'autonomy_decide',
                 'autonomy_told', 'autonomy_myself', 'autonomy_choice'],
    'Stress': ['stress_control', 'stress_overcome',
               'stress_confident', 'stress_way']
}

st.markdown('Breakdown of responses for your school')

chosen = data[
    (data['measure'].isin(constituents[chosen_variable])) &
    (data['school_lab'] == 'School A') &
    (data['year_group_lab'] == 'All') &
    (data['gender_lab'] == 'All') &
    (data['fsm_lab'] == 'All') &
    (data['sen_lab'] == 'All')]

df_list = []
for index, row in chosen.iterrows():
    df = pd.DataFrame(zip(literal_eval(row['cat_lab']),
                          literal_eval(row['percentage']),
                          literal_eval(row['count'])),
                      columns=['cat_lab', 'percentage', 'count'])
    df['measure'] = row['measure']
    df_list.append(df)
chosen_result = pd.concat(df_list)

fig = px.bar(
    chosen_result, x='percentage', y='measure', color='cat_lab',
    text_auto=True, title=chosen_variable, hover_data=['count'], orientation='h')
st.plotly_chart(fig, use_container_width=True)