import streamlit as st
from kailo_beewell_dashboard.page_setup import (
    page_setup, blank_lines, page_footer)
from kailo_beewell_dashboard.authentication import check_password
from kailo_beewell_dashboard.import_data import import_tidb_data
from kailo_beewell_dashboard.summary_rag import summary_intro, summary_table
from kailo_beewell_dashboard.reshape_data import get_school_size

# Set page configuration
page_setup()

if check_password():

    # Import the data from TiDB Cloud if not already in session state
    import_tidb_data()

    # Get data from session state
    counts = st.session_state.counts
    data = st.session_state.scores_rag

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

    # Introduction with guide to the RAG box and what they mean
    school_size = get_school_size(counts, st.session_state.school)
    summary_intro(school_size)

    # Blank space and header
    blank_lines(3)
    st.subheader('Choose what results to view')

    # Choose comparator
    chosen_group = st.selectbox(label='Show results:', options=[
        'For all pupils', 'By year group', 'By gender', 'By FSM', 'By SEN'])

    # Blank space and header
    blank_lines(3)
    st.subheader('Results')
    st.markdown('Click on a topic to view results in more detail.')
    blank_lines(1)

    # Grid with RAG rating for each topic, by chosen group
    summary_table(data, chosen_group, st.session_state.school)

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

    page_footer(st.session_state.school)
