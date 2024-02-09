import numpy as np
import pandas as pd
import streamlit as st
from utilities.switch_page_button import switch_page
from utilities.page_setup import page_setup, blank_lines
from utilities.authentication import check_password
from utilities.import_data import import_tidb_data
from utilities.summary_rag import summary_intro, result_box
from utilities.reshape_data import filter_by_group

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

    # Introduction with guide to the RAG box and what they mean
    summary_intro(st.session_state.school, counts)

    # Blank space and header
    blank_lines(3)
    st.subheader('Choose what results to view')

    # Choose variable and comparator
    chosen_group = st.selectbox(label='Show results:', options=[
        'For all pupils', 'By year group', 'By gender', 'By FSM', 'By SEN'])

    # Filter by chosen grouping and school
    chosen, pivot_var, order = filter_by_group(
        data, chosen_group, st.session_state.school, 'summary')
    # Filter to variable relevant for summary page
    chosen = chosen[~chosen['variable'].isin([
        'birth_you_age_score', 'overall_count', 'staff_talk_score', 
        'home_talk_score', 'peer_talk_score'])]

    if chosen_group != 'For all pupils':
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
                if ((row.iloc[i] in ['below', 'average', 'above']) |
                        pd.isnull(row.iloc[i])):
                    result_box(row.iloc[i])
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
