'''
Helper function for setting up the page, with the same settings for every page.
'''
import streamlit as st

def page_setup(layout):
    '''
    Set up page to standard conditions, with layout as specified
    Inputs:
    - layout: string, 'wide' or 'centered'
    '''
    st.set_page_config(
        page_title='#BeeWell School Dashboard',
        page_icon='🐝',
        initial_sidebar_state='expanded',
        layout=layout,
        menu_items={'About': 'Dashboard for schools completing the standard version of the #BeeWell survey in North Devon and Torridge in 2023/24.'})

    # Add logo to sidebar
    st.sidebar.image('images/kailo_beewell_logo.png', output_format='PNG')

    # Import CSS style
    with open('css/style.css') as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)