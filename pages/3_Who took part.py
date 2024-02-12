import streamlit as st
from utilities.page_setup import page_setup, blank_lines
from utilities.authentication import check_password
from utilities.import_data import import_tidb_data
from utilities.reshape_data import get_school_size
from utilities.who_took_part import (
    create_demographic_page_intro,
    demographic_plots)

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

    # Create the figures (with their titles and descriptions)
    demographic_plots(dem_prop, st.session_state.school, chosen_group)

    # Filter to results from current school
    chosen = dem_prop[dem_prop['school_lab'] == st.session_state.school]