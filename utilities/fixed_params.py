'''
Helper function for setting up the page, with the same settings for every page.
'''
import streamlit as st

def page_setup():
    st.set_page_config(
        page_title='#BeeWell School Dashboard',
        page_icon='🐝',
        initial_sidebar_state='expanded',
        layout='wide')