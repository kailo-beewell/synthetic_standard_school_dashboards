import streamlit as st
from utilities.page_setup import page_setup
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
    create_bar_charts
)

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

    ###############################################################################
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

    ###############################################################################
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
    st.write('')
    st.write('')

    # Topic header and description
    st.divider()
    write_topic_intro(chosen_variable, chosen_variable_lab, df_scores)
    st.write('')

    ###############################################################################
    # Breakdown of question responses chart

    # Section header and description
    write_response_section_intro(chosen_variable_lab)

    # Get dataframe with results for the chosen variable, group and school
    chosen_result = get_chosen_result(
        chosen_variable, chosen_group, df_prop, st.session_state.school)

    # Produce bar charts with accompanying chart section descriptions, and titles
    create_bar_charts(chosen_variable, chosen_result)
    st.text('')
    st.text('')
    st.text('')

    ###############################################################################
    # Comparator chart between schools...

    # Filter to relevant school and get total school size to use in text with chart
    school_counts = counts.loc[counts['school_lab'] == st.session_state.school]
    school_size = school_counts.loc[
        (school_counts['year_group_lab'] == 'All') &
        (school_counts['gender_lab'] == 'All') &
        (school_counts['fsm_lab'] == 'All') &
        (school_counts['sen_lab'] == 'All'), 'count'].values[0].astype(int)

    # Create dataframe based on chosen variable
    between_schools = df_scores[
        (df_scores['variable'].str.replace('_score', '') == chosen_variable) &
        (df_scores['year_group_lab'] == 'All') &
        (df_scores['gender_lab'] == 'All') &
        (df_scores['fsm_lab'] == 'All') &
        (df_scores['sen_lab'] == 'All')]

    # Get count of pupils who completed the topic questions
    topic_count = int(between_schools.loc[
        between_schools['school_lab'] == st.session_state.school, 'count'].to_list()[0])

    # Get RAG rating for that school
    devon_rag = between_schools.loc[
        between_schools['school_lab'] == st.session_state.school, 'rag'].to_list()[0]

    # Header and description of section
    st.subheader('Comparison with other schools')
    st.markdown(f'''
    In this section, an overall score for the topic of
    '{chosen_variable_lab.lower()}' has been calculated for each pupil with complete
    responses on this question. For this topic, your school had {topic_count} complete
    responses (out of a possible {school_size}).

    Possible scores for each pupil on this topic range from 
    {score_descriptions[chosen_variable][0]} with **higher scores indicating
    {score_descriptions[chosen_variable][1]}** - and vice versa for lower scores.

    The mean score of the pupils at you school is compared with pupils who completed
    the same survey questions at other schools. This allows you to see whether the 
    score for pupils at your school is average, below average or above average.
    This matches the scores presented on the 'Summary' page.''')

    # Add box with RAG rating to the page
    st.markdown(f'The average score for {chosen_variable_lab.lower()} at your school, compared to other schools in Northern Devon, was:')
    if devon_rag == 'below':
        st.error('Below average')
    elif devon_rag == 'average':
        st.warning('Average')
    elif devon_rag == 'above':
        st.success('Above average')

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
    # When comparing to the Greater Manchester data, be aware that (i) there are
    # likely to be greater differences in population characteristics between
    # Northern Devon and Greater Manchester than between different areas in
    # Northern Devon, and (ii) the Greater Manchester data were collected in Autumn
    # Term 2021 while the Havering data was collected in Summer Term 2023. 
