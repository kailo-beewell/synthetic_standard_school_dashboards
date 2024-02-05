'''
Helper functions for the explore_results() page. This is in addition to the
functions in bar_charts.py and bar_charts_text.py. They are utilised for the
streamlit pages and PDF report, and help to streamline code that would be
repeated between those two outputs, and ensure any changes are made to both.
'''
import pandas as pd
import streamlit as st


def create_topic_dict(df):
    '''
    Generate dictionary of survey topics with keys as the topic labels 
    ('variable_lab') and values as the raw topic strings ('variable').

    Parameters
    ----------
    df : pandas dataframe
        Dataframe containing the 'variable' and 'variable_lab' columns

    Returns
    -------
    topic_dict : dictionary
        Dictionary to map between topic raw names and label names
    '''
    # Get dataframe with the unique variables and their labels
    topic_df = df[['variable', 'variable_lab']].drop_duplicates()

    # Drop topics that we don't want to appear in the dictionary
    topic_df = topic_df[~topic_df['variable'].isin([
            'staff_talk_score', 'home_talk_score', 'peer_talk_score'])]

    # Remove the '_score' suffix from the variable names
    topic_df['variable'] = topic_df['variable'].str.replace('_score', '')

    # Convert to a dictionary
    topic_dict = pd.Series(
        topic_df.variable.values, index=topic_df.variable_lab).to_dict()

    return topic_dict


def write_topic_intro(chosen_variable, chosen_variable_lab, df,
                      output='streamlit', content=None):
    '''
    Writes the header for the topic on the Explore Results streamlit page or
    in HTML for page of PDF report.
    Example output: 
        Psychological Wellbeing
        These questions are about how positive and generally happy young people
        feel regarding their life.

    Parameters
    ----------
    chosen_variable : string
        Chosen variable in simple format (e.g. 'psychological_wellbeing')
    chosen_variable_lab : string
        Chosen variable in label format (e.g. 'Psychological wellbeing')
    df : pandas dataframe
        Dataframe containing the 'variable' and 'description' columns for each topic.
    output : string
        Specifies whether to write for 'streamlit' (default) or 'pdf'.
    content : list
        Optional input used when output=='pdf', contains HTML for report.

    Returns
    -------
    content : list
        Optional return, used when output=='pdf', contains HTML for report.
    '''
    # Header (name of topic)
    if output=='streamlit':
        st.markdown(f'''<h2 style='font-size:55px;text-align:center;'>{
            chosen_variable_lab}</h2>''', unsafe_allow_html=True)
    elif output=='pdf':
        content.append(f'''<h2 style='text-align:center;'>{
            chosen_variable_lab}</h2>''')

    # Description under header (one sentence summary of topic)
    # Create dictionary where key is topic name and value is topic description
    description = (df[['variable', 'description']]
                   .drop_duplicates()
                   .set_index('variable')
                   .to_dict()['description'])

    # Create description string
    topic_descrip = f'''
<p style='text-align:center;'><b>These questions are about
{description[f'{chosen_variable}_score'].lower()}</b></p>'''

    # Print that description string into streamlit page or PDF report HTML
    if output=='streamlit':
        st.markdown(topic_descrip, unsafe_allow_html=True)
    elif output=='pdf':
        content.append(f'{topic_descrip}<br>')
        return content


def write_response_section_intro(
        chosen_variable_lab, output='streamlit', content=None):
    '''
    Create the header and description for the section with the bar charts
    showing responses from pupils to each question of a topic.
    Example output: 
        Responses from pupils at your school
        In this section, you can see how pupils at you school responded to 
        survey questions that relate to the topic of 'psychological wellbeing'.

    Parameters
    ----------
    chosen_variable_lab : string
        Chosen variable in label format (e.g. 'Psychological wellbeing')
    output : string
        Specifies whether to write for 'streamlit' (default) or 'pdf'.
    content : list
        Optional input used when output=='pdf', contains HTML for report.

    Returns
    -------
    content : list
        Optional return, used when output=='pdf', contains HTML for report.
    '''
    # Section
    header = 'Responses from pupils at your school'
    if output=='streamlit':
        st.subheader(header)
    elif output=='pdf':
        content.append(f'<h3>{header}</h3>')

    # Section description
    section_descrip = f'''
In this section, you can see how pupils at you school responded to survey
questions that relate to the topic of '{chosen_variable_lab.lower()}'.'''
    if output=='streamlit':
        st.markdown(section_descrip)
    elif output=='pdf':
        content.append(f'<p>{section_descrip}</p>')
        return content