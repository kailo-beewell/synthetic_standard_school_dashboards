'''
Helper function for setting up the page, with the same settings for every page.
'''
import base64
import streamlit as st

def page_setup():
    '''
    Set up page to standard conditions, with layout as specified
    '''
    st.set_page_config(
        page_title='#BeeWell School Dashboard',
        page_icon='🐝',
        initial_sidebar_state='expanded',
        layout='centered',
        menu_items={'About': 'Dashboard for schools completing the standard version of the #BeeWell survey in North Devon and Torridge in 2023/24.'})

    # Add logo to sidebar, using markdown rather than st.sidebar.image as that
    # allows you to add alt_text for the image
    file = open('./images/kailo_beewell_logo.png', 'rb')
    contents = file.read()
    url = base64.b64encode(contents).decode('utf-8')
    file.close()
    st.sidebar.markdown(f'''
<img src='data:image/png;base64,{url}' 
alt='#BeeWell delivered by Kailo in Northern Devon'>''', unsafe_allow_html=True)

    # Import CSS style
    with open('css/style.css') as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)