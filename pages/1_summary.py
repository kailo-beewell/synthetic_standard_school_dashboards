import streamlit as st
from utilities.fixed_params import page_setup

# Set page configuration
page_setup()

st.title('''Your school's results''')

groups = st.selectbox('Results:', ['All pupils', 'By year group', 'By gender', 'By FSM', 'By SEN'])
comparator = st.selectbox('Compared against:', ['Other schools in Northern Devon'])

