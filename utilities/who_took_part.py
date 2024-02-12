'''
Helper functions for the 'Who took part' section of the dashboard and report
'''
import streamlit as st


def create_demographic_page_intro(school_size, output='streamlit'):
    '''
    Creates the title and introductory paragraph for the 'Who took part'
    demographic section of the dashboard/report

    Parameters
    ----------
    school_size : integer
        Total number of pupils who completed at least one question at school
    output : string
        Specifies whether to write for 'streamlit' (default) or 'pdf'.

    Returns
    -------
    html_string : string
        Optional return, used when output=='pdf', contains HTML for report.
    '''
    # Title
    title = 'Who took part?'

    # Introductory paragraph
    if output == 'streamlit':
        type = 'page'
    elif output == 'pdf':
        type = 'section'
    description = f'''
There were {school_size} pupils at your school who took part in the #BeeWell
survey. This {type} describes the sample of pupils who completed the survey.'''

    # Write to streamlit dashboard
    if output == 'streamlit':
        st.title(title)
        st.markdown(description)
    # Write to PDF report
    elif output == 'pdf':
        html_string = f'''
<div class='page'>
    <div class='section_container'>
        <h1 style='page-break-before:always;' id='who_took_part'>{title}</h1>
        <p>{description}</p>
    </div>
</div>'''
        return html_string


def demographic_headers():
    '''
    Creates dictionary of headers for the demographic section

    Returns
    -------
    header_dict : dictionary
        Dictionary where key is a variable name, and value is the header
    '''
    header_dict = {
        'year_group': 'Year group',
        'fsm': 'Eligible for free school meals (FSM)',
        'gender': 'Gender and transgender',
        'sexual_orientation': 'Sexual orientation',
        'care_experience': 'Care experience',
        'young_carer': 'Young carers',
        'neuro': 'Special educational needs and neurodivergence',
        'ethnicity': 'Ethnicity',
        'english_additional': 'English as an additional language',
        'birth': 'Background'}
    return header_dict