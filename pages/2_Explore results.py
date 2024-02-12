import streamlit as st
from utilities.page_setup import page_setup, blank_lines
from utilities.authentication import check_password
from utilities.bar_charts import details_ordered_bar
from utilities.score_descriptions import score_descriptions
from utilities.import_data import import_tidb_data
from utilities.explore_results import (
    write_page_title,
    create_topic_dict,
    write_topic_intro,
    write_response_section_intro,
    get_chosen_result,
    create_bar_charts,
    get_between_schools,
    write_comparison_intro
)
from utilities.reshape_data import get_school_size

# Set page configuration
page_setup()

if check_password():

    # Import the data from TiDB Cloud if not already in session state
    import_tidb_data()

    # Add name of school (to help with monitoring)
    st.markdown(st.session_state.school)

    # Assign the data from the session state
    df_scores = st.session_state.scores_rag
    df_prop = st.session_state.responses
    counts = st.session_state.counts

    ###########################################################################
    # Getting topics

    # Create dictionary of topics
    topic_dict = create_topic_dict(df_scores)

    # If session state doesn't contain chosen variable, default to Autonomy
    # If it does (i.e. set from Summary page), use that
    if 'chosen_variable_lab' not in st.session_state:
        st.session_state['chosen_variable_lab'] = 'Autonomy'

    # Convert topics to list and find index of the session state variable
    topic_list = list(topic_dict.keys())
    default = topic_list.index(st.session_state['chosen_variable_lab'])

    ###########################################################################
    # Page introduction

    write_page_title()

    # Select topic
    chosen_variable_lab = st.selectbox(
        '**Topic:**', topic_dict.keys(), index=default)

    # Convert from variable_lab to variable
    chosen_variable = topic_dict[chosen_variable_lab]

    # Select pupils to view results for
    chosen_group = st.selectbox(
        '**View results:**', ['For all pupils', 'By year group',
                              'By gender', 'By FSM', 'By SEN'])
    blank_lines(2)

    # Topic header and description
    st.divider()
    write_topic_intro(chosen_variable, chosen_variable_lab, df_scores)
    blank_lines(1)

    ###########################################################################
    # Responses to each question...

    # Section header and description
    write_response_section_intro(chosen_variable_lab)

    # Get dataframe with results for the chosen variable, group and school
    chosen_result = get_chosen_result(
        chosen_variable, chosen_group, df_prop, st.session_state.school)

    # Produce bar charts w/ accompanying chart section descriptions and titles
    create_bar_charts(chosen_variable, chosen_result)
    blank_lines(3)

    ###########################################################################
    # Comparator chart between schools...

    # Create dataframe based on chosen variable
    between_schools = get_between_schools(df_scores, chosen_variable)

    # Write the comparison intro text (title, description, RAG rating)
    school_size = get_school_size(counts, st.session_state.school)
    write_comparison_intro(
        school_size, st.session_state.school, chosen_variable,
        chosen_variable_lab, score_descriptions, between_schools)

    # Create ordered bar chart
    details_ordered_bar(between_schools, st.session_state.school)

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

    # Draft phrasing for benchmarking (not currently included in dashboards):
    # When comparing to the Greater Manchester data, be aware that (i) there
    # are likely to be greater differences in population characteristics
    # between Northern Devon and Greater Manchester than between different
    # areas in Northern Devon, and (ii) the Greater Manchester data were
    # collected in Autumn Term 2021 while the Havering data was collected in
    # Summer Term 2023.
