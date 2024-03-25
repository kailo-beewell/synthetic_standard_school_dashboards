from kailo_beewell_dashboard.authentication import check_password
from kailo_beewell_dashboard.explore_results import (
    choose_topic,
    create_bar_charts,
    write_comparison_intro,
    write_comparison_result,
    write_page_title,
    write_response_section_intro,
    write_topic_intro,
    get_chosen_result)
from kailo_beewell_dashboard.import_data import import_tidb_data
from kailo_beewell_dashboard.page_setup import (
    blank_lines, page_footer, page_setup)
from kailo_beewell_dashboard.reshape_data import filter_by_group
from kailo_beewell_dashboard.reuse_text import caution_comparing
from kailo_beewell_dashboard.score_descriptions import score_descriptions
import streamlit as st

# Set page configuration
page_setup('standard')

if check_password('standard'):

    # Import the data from TiDB Cloud if not already in session state
    import_tidb_data('standard')

    # Assign the data from the session state
    df_scores = st.session_state.scores_rag
    df_prop = st.session_state.responses
    counts = st.session_state.counts

    #####################
    # Page introduction #
    #####################

    write_page_title()

    # Select topic
    chosen_variable_lab, chosen_variable = choose_topic(
        df_scores, include_raw_name=True)

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
    st.markdown(caution_comparing(type='school'))

    page_footer(st.session_state.school)
