import streamlit as st
from utilities.fixed_params import page_setup

# Set page configuration
page_setup()

st.title('''Autonomy''')

# Currently not used, only one selection
group = st.selectbox('Results', ['All pupils'])

st.markdown('Breakdown of responses for your school')