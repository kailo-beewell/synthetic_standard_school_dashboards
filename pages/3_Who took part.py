import streamlit as st
from kailo_beewell_dashboard.page_setup import (
    page_setup, blank_lines, page_footer)
from kailo_beewell_dashboard.authentication import check_password
from kailo_beewell_dashboard.import_data import import_tidb_data
from kailo_beewell_dashboard.reshape_data import get_school_size
from kailo_beewell_dashboard.who_took_part import (
    create_demographic_page_intro, demographic_plots)

# Set page configuration
page_setup('standard')

if check_password('standard'):

    # Import the data from TiDB Cloud if not already in session state
    import_tidb_data('standard')

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

    page_footer(st.session_state.school)
