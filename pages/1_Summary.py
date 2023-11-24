import numpy as np
import pandas as pd
import streamlit as st
from utilities.fixed_params import page_setup

# Set page configuration
page_setup('centered')

# Manually set school (will need to change to set globally on login)
school = 'School B'

# Set font size
font_size = 18

st.title('''Summary of your school's results''')
st.subheader('Introduction')
st.markdown('This shows how the answers of pupils at your school compare with pupils from other schools. You can choose to compare against either the other schools in Northern Devon, or to matched schools from across the country.')

cols = st.columns([0.333, 0.666])
with cols[0]:
    st.error('↓ Below average')
with cols[1]:
    st.markdown('This means that average scores for students in your school are **worse** than average scores for pupils at other schools')

cols = st.columns([0.333, 0.666])
with cols[0]:
    st.warning('~ Average')
with cols[1]:
    st.markdown('This means that average scores for students in your school are **similar** to average scores for pupils at other schools')

cols = st.columns([0.333, 0.666])
with cols[0]:
    st.success('↑ Above average')
with cols[1]:
    st.markdown('This means that average scores for students in your school are **better** than average scores for pupils at other schools')

cols = st.columns([0.333, 0.666])
with cols[0]:
    st.info('n<10')
with cols[1]:
    st.markdown('This means that **less than ten** students in your school completed questions for this topic, so the results cannot be shown.')

##########################################################

# Import data
data = pd.read_csv('data/survey_data/aggregate_scores_rag.csv')

# Space and header
st.markdown('#')
st.subheader('Choose what results to view')

# Set label style using components API
def change_label_style(label, font_size='12px', font_color='black', font_family='sans-serif'):
    html = f"""
    <script>
        var elems = window.parent.document.querySelectorAll('p');
        var elem = Array.from(elems).find(x => x.innerText == '{label}');
        elem.style.fontSize = '{font_size}';
        elem.style.color = '{font_color}';
        elem.style.fontFamily = '{font_family}';
    </script>
    """
    st.components.v1.html(html)

# Choose variable and comparator
label = 'Results:'
chosen_group = st.selectbox(label, ['All pupils', 'By year group', 'By gender', 'By FSM', 'By SEN'])
change_label_style(label, '18px')
label = 'Compared against:'
comparator = st.selectbox(label, ['Other schools in Northern Devon', 'Matched schools from across the country'])
change_label_style(label, '18px')

# Filter data depending on choice
year_group = ['All']
gender = ['All']
fsm = ['All']
sen = ['All']
if chosen_group == 'By year group':
    pivot_var = 'year_group_lab'
    year_group = ['Year 8', 'Year 10']
    order = ['Year 8', 'Year 10']
elif chosen_group == 'By gender':
    pivot_var = 'gender_lab'
    gender = ['Girl', 'Boy']
              #'I describe myself in another way', 'Non-binary',
              #'Prefer not to say']
    order = ['Girl', 'Boy']
elif chosen_group == 'By FSM':
    pivot_var = 'fsm_lab'
    fsm = ['FSM', 'Non-FSM']
    order = ['FSM', 'Non-FSM']
elif chosen_group == 'By SEN':
    pivot_var = 'sen_lab'
    sen = ['SEN', 'Non-SEN']
    order = ['SEN', 'Non-SEN']

# Filter data
chosen = data[
    (data['school_lab'] == school) &
    (data['year_group_lab'].isin(year_group)) &
    (data['gender_lab'].isin(gender)) &
    (data['fsm_lab'].isin(fsm)) &
    (data['sen_lab'].isin(sen)) &
    (~data['variable'].isin([
        'birth_you_age_score', 'overall_count', 'staff_talk_score',
        'home_talk_score', 'peer_talk_score']))]

if chosen_group != 'All pupils':
    # Pivot from wide to long whilst maintaining row order
    chosen = pd.pivot_table(
        chosen[['variable_lab', pivot_var, 'rag', 'description']],
        values='rag', index=['variable_lab', 'description'], columns=pivot_var,
        aggfunc='sum', sort=False).reset_index().replace(0, np.nan)
    # Reorder columns
    chosen = chosen[['variable_lab'] + order + ['description']]
else:
    chosen = chosen[['variable_lab', 'rag', 'description']]


##########################################################

st.markdown('#')
st.subheader('Results')

description = chosen['description']
chosen = chosen.drop('description', axis=1)

# Set number of columns
ncol = len(chosen.columns)

# Rename columns if in the dataframe
colnames = {
    'variable_lab': 'Topic',
    'rag': 'All pupils',
}
chosen = chosen.rename(columns=colnames)

# Set up columns with custom dimensions if just 2
if ncol == 2:
    cols = st.columns([0.333, 0.333, 0.333])
else:
    cols = st.columns(ncol)

# Add column names
for i in range(ncol):
    with cols[i]:
        st.markdown('**' + chosen.columns[i] + '**')

# For each row of dataframe, create streamlit columns and write data from cell
for index, row in chosen.iterrows():
    if ncol == 2:
        cols = st.columns([0.333, 0.333, 0.333])
    else:
        cols = st.columns(ncol)
    for i in range(ncol):
        with cols[i]:
            if row[i] == 'below':
                st.error('↓ Below average')
            elif row[i] == 'average':
                st.warning('~ Average')
            elif row[i] == 'above':
                st.success('↑ Above average')
            elif pd.isnull(row[i]):
                st.info('n<10')
            else:
                st.markdown('')
                st.markdown('**' + row[i] + '**', help=description[index])

