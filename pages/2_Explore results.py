import streamlit as st
from kailo_beewell_dashboard.page_setup import (
    page_setup, blank_lines, page_footer)
from kailo_beewell_dashboard.authentication import check_password
from kailo_beewell_dashboard.score_descriptions import score_descriptions
from kailo_beewell_dashboard.import_data import import_tidb_data
from kailo_beewell_dashboard.explore_results import (
    write_page_title,
    create_topic_dict,
    write_topic_intro,
    write_response_section_intro,
    get_chosen_result,
    create_bar_charts,
    write_comparison_intro,
    write_comparison_result)
from kailo_beewell_dashboard.reshape_data import filter_by_group
from kailo_beewell_dashboard.reuse_text import reuse_text

# Set page configuration
page_setup('standard')

if check_password():

    # Import the data from TiDB Cloud if not already in session state
    import_tidb_data()

    # Assign the data from the session state
    df_scores = st.session_state.scores_rag
    df_prop = st.session_state.responses
    counts = st.session_state.counts

    ##################
    # Getting topics #
    ##################

    # Create dictionary of topics
    topic_dict = create_topic_dict(df_scores)

    # If session state doesn't contain chosen variable, default to Autonomy
    # If it does (i.e. set from Summary page), use that
    if 'chosen_variable_lab' not in st.session_state:
        st.session_state['chosen_variable_lab'] = 'Autonomy'

    # Convert topics to list and find index of the session state variable
    topic_list = list(topic_dict.keys())
    default = topic_list.index(st.session_state['chosen_variable_lab'])

    #####################
    # Page introduction #
    #####################

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

    #################################
    # Responses to each question... #
    #################################

    # Section header and description
    write_response_section_intro(chosen_variable_lab)

    # Get dataframe with results for the chosen variable, group and school
    chosen_result = get_chosen_result(
        chosen_variable, chosen_group, df_prop, st.session_state.school)

    # Produce bar charts w/ accompanying chart section descriptions and titles
    create_bar_charts(chosen_variable, chosen_result)
    blank_lines(3)

    #######################################
    # Comparator chart between schools... #
    #######################################

    # Create dataframe based on chosen variable
    between_schools, group_lab, order = filter_by_group(
        df=df_scores, chosen_group=chosen_group, output='compare',
        chosen_variable=chosen_variable+'_score')

    # Write the comparison introduction
    write_comparison_intro(
        chosen_variable, chosen_variable_lab, score_descriptions)

    # Filter to each group (will just be 'all' if was for all pupils), then
    # print the results and create the ordered bar chart for each
    for group in order:
        blank_lines(1)
        group_result = between_schools[between_schools[group_lab] == group]
        with st.container(border=True):
            write_comparison_result(
                st.session_state.school, group_result, group)

    # Add caveat for interpretation
    blank_lines(1)
    st.subheader('Recommendation when making comparisons')
    st.markdown(reuse_text['caution_comparing'])

    page_footer(st.session_state.school)
