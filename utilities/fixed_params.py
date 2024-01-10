'''
Helper function for setting up the page, with the same settings for every page.
'''
import base64
import streamlit as st

def page_logo():
    '''
    Create logo to go above the pages in the sidebar
    '''
    # Set up logo for display in markdown, which we use instead of st.image()
    # to allow inline display and alt_text
    file = open('./images/kailo_beewell_logo_padded.png', 'rb')
    contents = file.read()
    url = base64.b64encode(contents).decode('utf-8')
    file.close()

    # Display logo
    st.markdown(f'''
<style>
    [data-testid='stSidebarNav'] {{
        background-image: url('data:image/png;base64,{url}');
        background-repeat: no-repeat;
        padding-top: 110px; /* Move page names down */
        background-position: 0px 50px; /* Move image down */
        background-size: 240px;
    }}
    
</style>
''', unsafe_allow_html=True)

def page_setup():
    '''
    Set up page to standard conditions, with layout as specified
    '''
    # Set up streamlit page parameters
    st.set_page_config(
        page_title='#BeeWell School Dashboard',
        page_icon='🐝',
        initial_sidebar_state='expanded',
        layout='centered',
        menu_items={'About': 'Dashboard for schools completing the standard version of the #BeeWell survey in North Devon and Torridge in 2023/24.'})

    # Temporary: manual force School B when open page
    st.session_state.school = 'School B'

    # Import CSS style
    with open('css/style.css') as css:
        st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

    # Add page logo
    page_logo()
