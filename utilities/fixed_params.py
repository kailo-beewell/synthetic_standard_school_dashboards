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

    # Set up logo for display in markdown, which we use instead of st.image()
    # to allow inline display and alt_text
    file = open('./images/kailo_beewell_logo.png', 'rb')
    contents = file.read()
    url = base64.b64encode(contents).decode('utf-8')
    file.close()

    # Temporary: manual force School B when open page
    st.session_state.school = 'School B'

    # Add logo and school name to top of each page
    with st.sidebar:
        st.markdown(f'''<img src='data:image/png;base64,{url}' 
                    alt='#BeeWell delivered by Kailo in Northern Devon'>''',
                    unsafe_allow_html=True)
        # Manually set school (will need to change to set globally on login)
        st.session_state.school = st.radio(
            label='School (for testing)',
            options=['School A', 'School B', 'School C', 'School D',
                     'School E', 'School F', 'School G'],
            index=1)

    # Blank space
    st.markdown('')

    # Import CSS style
    with open('css/style.css') as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)