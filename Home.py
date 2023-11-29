import pandas as pd
import streamlit as st
from st_pages import Page, show_pages
from PIL import Image
from utilities.switch_page_button import switch_page
from utilities.fixed_params import page_setup

# Set page configuration
page_setup('centered')

#st.markdown(
 #   """
 #   <style>
 #   .sidebar .sidebar-content {
 #       font-size: 50px;
 #   }
 #   </style>
 #   """,
 #   unsafe_allow_html=True
#)

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page('Home.py', 'Home', "🏠"),
        Page('pages/1_Summary.py', 'Summary'),
        Page('pages/Details.py', 'Details'),
        Page('pages/3_About.py', 'About', in_section=False)
    ]
)

st.write(
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" />',
    unsafe_allow_html=True,
)

st.markdown(
    """

<style>
    .css-8hkptd {
        font-family: 'Material Symbols Outlined';
        font-weight: normal;
        font-style: normal;
        font-size: 24px;
        line-height: 1;
        letter-spacing: normal;
        text-transform: none;
        display: inline-block;
        white-space: nowrap;
        word-wrap: normal;
        direction: ltr;
        -webkit-font-feature-settings: 'liga';
        -webkit-font-smoothing: antialiased;
        color: black !important;
    }
</style>
    """,
    unsafe_allow_html=True,
)

# THIS CHANGES THE BACKGROUND COLOUR, but not the line height or font size of the categories
# only the changeable text down below... perhaps it's because I'm doing this and st.pages?
# Need to try out without st.pages
# Need to try with st.pages
# Need to try removing all page links from the sidebar and just creating my own with
# markdown as maybe then I could control font size and stuff without the overarching css styles
st.markdown("""
<style>
    [data-testid=stSidebar] {
        line-height: 5;
        font-size: 50px;
        background-color: #ff000050;
    }
</style>
""", unsafe_allow_html=True)

# THIS DOES NOT SEEM TO
#st.markdown(
#    """
#<style>
#.css-nzvw1x {
#    background-color: #061E42 !important;
#    background-image: none !important;
#}
#.css-1aw8i8e {
#    background-image: none !important;
#    color: #FFFFFF !important
#}
#.css-ecnl2d {
#    background-color: #496C9F !important;
#    color: #496C9F !important
#}
#.css-15zws4i {
#    background-color: #496C9F !important;
#    color: #FFFFFF !important
#}
#</style>
#""",
#    unsafe_allow_html=True
#)

with st.sidebar:
    "## This is the sidebar"

###############################################################################

# Import data and images used on this page
data = pd.read_csv('data/survey_data/aggregate_scores.csv')
# illustration = Image.open('images/levelling-the-ground.jpg')

# Manually set school (will need to change to set globally on login)
school = 'School B'

################################################################################
with open('css/style.css') as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)
st.markdown('''<h1 style='text-align: center;'>School</h1>''', unsafe_allow_html=True)
################################################################################

st.markdown('''
Thank you for taking part in the #BeeWell survey. This dashboard contains results from pupils at your school, compared with other schools in Northern Devon, and matched schools from across the country.
''')

st.subheader('Guide to the dashboard')
st.markdown('Use the sidebar on the left to navigate to different pages of the dashboard.')

cols = st.columns([0.3, 0.7])
with cols[0]:
    if st.button('Summary'):
        switch_page('summary')
with cols[1]:
    st.markdown('This page gives an overview of how the average results at your school compare with other school, for all pupils and by pupil groups (year group, gender, FSM, SEN).')

cols = st.columns([0.3, 0.7])
with cols[0]:
    if st.button('Details'):
        switch_page('details')
with cols[1]:
    st.markdown('This page provides a breakdown of responses to each question.')

cols = st.columns([0.3, 0.7])
with cols[0]:
    st.info('Pupils')
with cols[1]:
    st.markdown('This page shows the characteristics of pupils who completed the survey at your school, compared with other schools.')

cols = st.columns([0.3, 0.7])
with cols[0]:
    st.info('About')
with cols[1]:
    st.markdown('This page contains background information about the survey.')

#if st.button('Summary'):
#    switch_page('summary')

# st.image(illustration)
st.subheader('FAQs')
with st.expander('How do I use this dashboard?'):
    st.write('Explanation')

with st.expander('How do I print or save a page as a PDF?'):
    st.write('There are several options...')

################################################################################
# Attempts at customising appearance...

st.sidebar.title('Title text')
st.sidebar.markdown('Markdown text')
st.selectbox('Example', ['aa', 'bb', 'cc'])
st.selectbox('Example 2', ['aa', 'bb', 'cc'])

st.metric('Metric title', 'Metric value', 'Metric change')
st.metric('Wind', '9mph', '-8%')

#def local_css(file_name):
#    with open(file_name) as f:
#        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

#def main():
#    local_css('css/style.css')

#if __name__ == '__main__':
#    main()

# Replace the markdown on the specified object
#with open('css/style.css') as f:
#    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)