'''
Helper functions for the summary page, and for the production of the 'RAG'
boxes which are also use on the 'Explore Results' page
'''
import pandas as pd
import streamlit as st
import numpy as np
from markdown import markdown


def html_rag_container(text, background, font):
    '''
    Generates a HTML container with the specified background and font colours,
    including the text provided, and with class of 'result_box'

    Parameters
    ----------
    text : string
        Text to go in the container
    background : string
        Background colour
    font : string
        Font colour

    Returns
    -------
    html_string : string
        HTML string, to be appended to the content for the report
    '''
    html_string = f'''
<div class='result_box' style='background: {background}; color: {font}'>
    <p>{text}</p>
</div>'''
    return html_string


def result_box(rag, output='streamlit'):
    '''
    Creates a result box with the RAG rating

    Parameters
    ----------
    rag : string
        Result from comparison with other schools - either 'below', 'average',
        'above', or np.nan
    output : string
        Specifies whether to write for 'streamlit' (default) or 'pdf'.

    Returns
    -------
    html_string : string
        HTML string, to be appended to the content for the report
    '''
    # Below average
    if rag == 'below':
        rag_text = 'Below average'
        if output == 'streamlit':
            st.error(rag_text)
        elif output == 'pdf':
            html_string = html_rag_container(rag_text, '#FFCCCC', '#95444B')

    # Average
    elif rag == 'average':
        rag_text = 'Average'
        if output == 'streamlit':
            st.warning(rag_text)
        elif output == 'pdf':
            html_string = html_rag_container(rag_text, '#FFE8BF', '#AA7A18')

    # Above average
    elif rag == 'above':
        rag_text = 'Above average'
        if output == 'streamlit':
            st.success(rag_text)
        elif output == 'pdf':
            html_string = html_rag_container(rag_text, '#B6E6B6', '#2B7C47')

    # Less than 10 responses
    elif pd.isnull(rag):
        rag_text = 'n < 10'
        if output == 'streamlit':
            st.info(rag_text)
        elif output == 'pdf':
            html_string = html_rag_container(rag_text, '#DCE4FF', '#19539A')

    if output == 'pdf':
        return html_string


def rag_intro_column(rag, rag_descrip, output='streamlit'):
    '''
    Generate a row for the introduction to the summary section, with a RAG
    box and description of that box across 2 columns.

    Parameters
    ----------
    rag : string
        RAG performance - either 'above', 'average', 'below', or np.nan
    rag_descrip : string
        Description of the RAG rating
    output : string
        Specifies whether to write for 'streamlit' (default) or 'pdf'.

    Returns
    -------
    html_string : string
        Section of HTML that creates the RAG introductory columns
    '''
    # Streamlit version
    if output == 'streamlit':
        cols = st.columns(2)
        with cols[0]:
            result_box(rag)
        with cols[1]:
            st.markdown(rag_descrip)

    # PDF version
    elif output == 'pdf':
        rag_box = result_box(rag, output='pdf')
        html_string = f'''
<div class='row'>
    <div class='column' style='margin-top:0.5em;'>
        {rag_box}
    </div>
    <div class='column'>
        {rag_descrip}
    </div>
</div>
'''
        return html_string


def summary_intro(chosen_school, counts, output='streamlit'):
    '''
    Creates the introduction for the summary section

    Parameters
    ----------
    chosen_school : string
        Name of chosen school
    counts : dataframe
        Dataframe with counts of pupils at each school
    output : string
        Specifies whether to write for 'streamlit' (default) or 'pdf'

    Returns
    -------
    html_string : string
        Optional return, if output=='pdf', contains HTML for summary cover page
    '''
    # For PDF report, create temporary list to store HTML for page
    if output == 'pdf':
        temp_content = []

    # Write title for this section
    title = '''Summary of your school's results'''
    if output == 'streamlit':
        st.title(title)
        st.subheader('Introduction')
    elif output == 'pdf':
        temp_content.append(f'''<h1 style='page-break-before:always;'
                            id='summary'>{title}</h1>''')

    # Filter to relevant school and get total school size
    school_counts = counts.loc[counts['school_lab'] == chosen_school]
    school_size = school_counts.loc[
        (school_counts['year_group_lab'] == 'All') &
        (school_counts['gender_lab'] == 'All') &
        (school_counts['fsm_lab'] == 'All') &
        (school_counts['sen_lab'] == 'All'), 'count'].values[0].astype(int)

    # Write introductory sentence for summary section
    descrip = f'''
At your school, a total of {school_size} pupils took part in the #BeeWell
survey. This page shows how the answers of pupils at your school compare with
pupils from other schools in Northern Devon.'''
    if output == 'streamlit':
        st.markdown(descrip)
    elif output == 'pdf':
        temp_content.append(f'<p>{descrip}</p>')

    # Write interpretation of each of the rag boxes
    rag_descrip_below = '''
This means that average scores for students in your school are **worse** than
average scores for pupils at other schools.'''
    rag_descrip_average = '''
This means that average scores for students in your school are **similar** to
average scores for pupils at other schools.'''
    rag_descrip_above = '''
This means that average scores for students in your school are **better** than
average scores for pupils at other schools.'''
    rag_descrip_small = '''
This means that **less than ten** students in your school completed questions
for this topic, so the results cannot be shown.'''
    if output == 'streamlit':
        rag_intro_column('below', rag_descrip_below)
        rag_intro_column('average', rag_descrip_average)
        rag_intro_column('above', rag_descrip_above)
        rag_intro_column(np.nan, rag_descrip_small)
    elif output == 'pdf':
        temp_content.append(
            rag_intro_column('below', markdown(rag_descrip_below), 'pdf'))
        temp_content.append(
            rag_intro_column('average', markdown(rag_descrip_average), 'pdf'))
        temp_content.append(
            rag_intro_column('above', markdown(rag_descrip_above), 'pdf'))
        temp_content.append(
            rag_intro_column(np.nan, markdown(rag_descrip_small), 'pdf'))

    # Write caveat re: sample size
    caveat = f'''
*Please note that  although a total of {school_size} pupils took part, the
topic summaries below are based only on responses from pupils who completed all
the questions of a given topic. The count of pupils who completed a topic is
available on each topic's "Explore results" page. However, the other figures
on the "Explore results" page present data from all pupils who took part.*'''
    if output == 'streamlit':
        st.markdown(caveat)
    elif output == 'pdf':
        temp_content.append(markdown(caveat))

    # For PDF report, format into section container and return
    if output == 'pdf':
        html_string = f'''
    <div class='page'>
        <div class='section_container'>
            {''.join(temp_content)}
        </div>
    </div>
    '''
        return html_string
