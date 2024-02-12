import streamlit as st
from utilities.page_setup import page_setup, blank_lines
from utilities.authentication import check_password
from utilities.bar_charts import survey_responses
from utilities.bar_charts_text import create_response_description
from utilities.import_data import import_tidb_data
from utilities.reshape_data import get_school_size, extract_nested_results
from utilities.who_took_part import create_demographic_page_intro

# Set page configuration
page_setup()

if check_password():

    # Import the data from TiDB Cloud if not already in session state
    import_tidb_data()

    # Add name of school (to help with monitoring)
    st.markdown(st.session_state.school)

    # Assign data from the session state
    dem_prop = st.session_state.demographic
    counts = st.session_state.counts

    ###########################################################################
    # Introduction including total pupil number

    # Get total pupil number
    school_size = get_school_size(counts, st.session_state.school)

    # Write title and introduction
    create_demographic_page_intro(school_size)
    blank_lines(1)

    # Select whether to view results alongside other schools or not
    chosen_group = st.selectbox(
        '**View results:**', ['For your school',
                              'Compared with other schools in Northern Devon'])
    blank_lines(2)

    ###########################################################################
    # Figures

    # Filter to results from current school
    chosen = dem_prop[dem_prop['school_lab'] == st.session_state.school]

    # If only looking at that school, drop the comparator school group data
    if chosen_group == 'For your school':
        chosen = chosen[chosen['school_group'] == 1]

    # Extract the nested lists in the dataframe
    chosen_result = extract_nested_results(
        chosen=chosen, group_lab='school_group_lab', plot_group=True)

    # Define headers for each of the plot groups - this will also define the
    # order in which these groups are shown
    header_dict = {
        'year_group': 'Year group',
        'fsm': 'Eligible for free school meals (FSM)',
        'gender': 'Gender and transgender',
        'sexual_orientation': 'Sexual orientation',
        'care_experience': 'Care experience',
        'young_carer': 'Young carers',
        'neuro': 'Special educational needs and neurodivergence',
        'ethnicity': 'Ethnicity',
        'english_additional': 'English as an additional language',
        'birth': 'Background'
    }

    # Import descriptions for the charts
    response_descrip = create_response_description()

    # This plots measures in loops, basing printed text on the measure names
    # and basing the titles of groups on the group names (which differs to the
    # survey responses page, which bases printed text on group names)
    for plot_group in header_dict.keys():

        # Add the title for that group
        st.header(header_dict[plot_group])

        # Find the measures in that group and loop through them
        measures = chosen_result.loc[
            chosen_result['plot_group'] == plot_group,
            'measure'].drop_duplicates()
        for measure in measures:

            # Add descriptive text if there is any
            if measure in response_descrip.keys():
                st.markdown(response_descrip[measure])

            # Filter to current measure and plot
            to_plot = chosen_result[chosen_result['measure'] == measure]
            survey_responses(to_plot)
