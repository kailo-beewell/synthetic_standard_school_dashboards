import numpy as np
import pandas as pd
import streamlit as st
from utilities.switch_page_button import switch_page
from utilities.page_setup import page_setup, blank_lines
from utilities.authentication import check_password
from utilities.import_data import import_tidb_data

# Set page configuration
page_setup()

if check_password():

    # Import the data from TiDB Cloud if not already in session state
    import_tidb_data()

    # Get data from session state
    counts = st.session_state.counts
    data = st.session_state.scores_rag

    # Add name of school (to help with monitoring)
    st.markdown(st.session_state.school)

    # Set button css for this page
    st.markdown('''
<style>
    /* Button */
    /* Set padding to match status elements, which are 16px but 14px matches */
    div.stButton > button:first-child
    {
        background-color: #F5F0ED;
        border-color: #F5F0ED;
        width: 100%;
        font-weight: bold;
        height: auto;
        padding-top: 14px !important;
        padding-bottom: 14px !important;
    }
</style>
''', unsafe_allow_html=True)

    ###########################################################################

    # Filter to relevant school and get total school size
    school_counts = counts.loc[counts['school_lab'] == st.session_state.school]
    school_size = school_counts.loc[
        (school_counts['year_group_lab'] == 'All') &
        (school_counts['gender_lab'] == 'All') &
        (school_counts['fsm_lab'] == 'All') &
        (school_counts['sen_lab'] == 'All'), 'count'].values[0].astype(int)

    st.title('''Summary of your school's results''')
    st.subheader('Introduction')
    st.markdown(f'''
At your school, a total of {school_size} pupils took part in the #BeeWell
survey. This page shows how the answers of pupils at your school compare with
pupils from other schools. You can choose to compare against either the other
schools in Northern Devon, or to matched schools from across the country.''')

    cols = st.columns([0.333, 0.666])
    with cols[0]:
        st.error('↓ Below average')
    with cols[1]:
        st.markdown('''
This means that average scores for students in your school are **worse** than
average scores for pupils at other schools''')

    cols = st.columns([0.333, 0.666])
    with cols[0]:
        st.warning('~ Average')
    with cols[1]:
        st.markdown('''
This means that average scores for students in your school are **similar** to
average scores for pupils at other schools''')

    cols = st.columns([0.333, 0.666])
    with cols[0]:
        st.success('↑ Above average')
    with cols[1]:
        st.markdown('''
This means that average scores for students in your school are **better** than
average scores for pupils at other schools''')

    cols = st.columns([0.333, 0.666])
    with cols[0]:
        st.info('n<10')
    with cols[1]:
        st.markdown('''
This means that **less than ten** students in your school completed questions
for this topic, so the results cannot be shown.''')

    # Print school size
    st.text('')
    st.markdown(f'''
*Please note that  although a total of {school_size} pupils took part, the
topic summaries below are based only on responses from pupils who completed all
the questions of a given topic. The count of pupils who completed a topic is
available on each topic's "Explore results" page. However, the other figures
on the "Explore results" page present data from all pupils who took part.*
''')

    ##########################################################

    # Blank space and header
    blank_lines(3)
    st.subheader('Choose what results to view')

    # Choose variable and comparator
    chosen_group = st.selectbox(label='Results:', options=[
        'All pupils', 'By year group', 'By gender', 'By FSM', 'By SEN'])

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
# 'I describe myself in another way', 'Non-binary', 'Prefer not to say']
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
        (data['school_lab'] == st.session_state.school) &
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
            values='rag', index=['variable_lab', 'description'],
            columns=pivot_var,
            aggfunc='sum', sort=False).reset_index().replace(0, np.nan)
        # Reorder columns
        chosen = chosen[['variable_lab'] + order + ['description']]
    else:
        chosen = chosen[['variable_lab', 'rag', 'description']]

    ##########################################################
    # Blank space and header
    blank_lines(3)
    st.subheader('Results')
    st.markdown('Click on a topic to view results in more detail.')
    blank_lines(1)

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

    # Set up columns
    cols = st.columns([0.3, 0.35, 0.35])

    # Add column names
    for i in range(ncol):
        with cols[i]:
            st.markdown(f'''
    <p style='text-align: center; font-weight: bold; font-size: 22px;'>
    {chosen.columns[i]}</p>
    ''', unsafe_allow_html=True)

    # For each row of dataframe, create streamlit columns and write data from
    # cell
    st.divider()
    for index, row in chosen.iterrows():
        cols = st.columns([0.3, 0.35, 0.35])
        st.divider()
        for i in range(ncol):
            # Create topic button or score
            with cols[i]:
                if row.iloc[i] == 'below':
                    st.error('↓ Below average')
                elif row.iloc[i] == 'average':
                    st.warning('~ Average')
                elif row.iloc[i] == 'above':
                    st.success('↑ Above average')
                elif pd.isnull(row.iloc[i]):
                    st.info('n<10')
                else:
                    # Create button that, if clicked, changes to details
                    if st.button(row.iloc[i]):
                        st.session_state['chosen_variable_lab'] = row.iloc[i]
                        switch_page('explore results')

    # Add caveat for interpretation
    st.subheader('Comparing between schools')
    st.markdown('''
Always be mindful when making comparisons between different schools. There are
a number of factors that could explain differences in scores (whether you are
above average, average, or below average). These include:
* Random chance ('one-off' findings).
* Differences in the socio-economic characteristics of pupils and the areas
where they live (e.g. income, education, ethnicity, access to services and
amenities).
* The number of pupils taking part - schools that are much smaller are more
likely to have more "extreme" results (i.e. above or below average), whilst
schools with a larger number of pupils who took part are more likely to
see average results

It's also worth noting that the score will only include results from pupils who
completed each of the questions used to calculate that topic - so does not
include any reflection of results from pupils who did not complete some or all
of the questions for that topic.
''')
