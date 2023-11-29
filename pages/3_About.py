import streamlit as st
from utilities.fixed_params import page_setup
import base64
from pathlib import Path

# Set page configuration
page_setup('wide')

st.title('About')

st.markdown('''
    Data information - will want to provide some details about calculations and
    data used within the dashboard, but likely finer details not necessary, and
    could instead be in a seperate document within the GitHub itself.''')

st.markdown('Also might want to link to other sites? https://kailo.community/. https://beewellprogramme.org/. Other dashboard.')

# Not working anymore - appears to be issue with iframe now as from - https://discuss.streamlit.io/t/using-st-markdown-to-show-embedded-pdf-file-gets-page-not-found/35527/6
# Think it's because I have interactive links and stuff
# Function for displaying PDF - move to utilities
def show_pdf(file_path):
    with open(file_path, 'rb') as f:
        # Open PDF file and encode with base64 encoding
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        # Embed in HTML iframe
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
        # Render in streamlit
        st.markdown(pdf_display, unsafe_allow_html=True)
# Display PDF containing full survey
# show_pdf('./pdfs/standard_beewell_survey_v2_1_devon.pdf')


with st.expander('Release Notes'):
    st.markdown(Path('changelog.md').read_text(), unsafe_allow_html=True)