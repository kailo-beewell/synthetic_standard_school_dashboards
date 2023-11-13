import streamlit as st

st.set_page_config(
    page_title='#BeeWell School Dashboard',
    page_icon='🐝',
    initial_sidebar_state='expanded'
)

st.title('''Your school's results''')

groups = st.selectbox('Results:', ['All pupils', 'By year group', 'By gender', 'By FSM', 'By SEN'])
comparator = st.selectbox('Compared against:', ['Other schools in Northern Devon'])

