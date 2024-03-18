from kailo_beewell_dashboard.about_page import create_about_page
from kailo_beewell_dashboard.authentication import check_password
from kailo_beewell_dashboard.page_setup import page_footer, page_setup
import streamlit as st

# Set page configuration
page_setup('standard')

# Check that viewer is logged in
if check_password('standard'):
    # Generate about page
    create_about_page('standard')
    # Add page footer
    page_footer(st.session_state.school)
