'''
Helper function for setting up the page, with the same settings for every page.
'''
import streamlit as st

def page_setup():
    st.set_page_config(
        page_title='#BeeWell School Dashboard',
        page_icon='🐝',
        initial_sidebar_state='expanded',
        layout='centered',
        menu_items={'About': 'Dashboard for schools completing the standard version of the #BeeWell survey in North Devon and Torridge in 2023/24.'})