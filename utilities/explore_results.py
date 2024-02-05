'''
Helper functions for the explore_results() page. This is in addition to the
functions in bar_charts.py and bar_charts_text.py. They are utilised for the
streamlit pages and PDF report, and help to streamline code that would be
repeated between those two outputs, and ensure any changes are made to both.
'''
import pandas as pd
import streamlit as st
from ast import literal_eval
import numpy as np
from utilities.bar_charts_text import create_response_description
from utilities.bar_charts import survey_responses


def write_page_title(output='streamlit', content=None):
    '''
    Writes the title of this page/section (Explore Results), for the streamlit
    page or for the PDF report.

    Parameters
    ----------
    output : string
        Specifies whether to write for 'streamlit' (default) or 'pdf'.
    content : list
        Optional input used when output=='pdf', contains HTML for report.

    Returns
    -------
    content : list
        Optional return, used when output=='pdf', contains HTML for report.
    '''
    # Title
    title = 'Explore results'
    if output=='streamlit':
        st.title(title)
    elif output=='pdf':
        temp_content = []
        temp_content.append(f'<h1>{title}</h1>')

    # Generate the description (with some changes to the text and spacing
    # between streamlit and the PDF report)
    if output=='streamlit':
        type1 = 'page'
        type2 = 'page'
        line_break = ''
    elif output=='pdf':
        type1 = 'section of the report'
        type2 = 'section'
        line_break = '<br><br>'
    descrip = f'''
This {type1} allows you to explore the results of pupils at your school.
{line_break} For each survey topic, you can see (a) a breakdown of how pupils
at your school responded to each question in that topic, and (b) a chart
building on results from the 'Summary' {type2} that allows you to understand
more about the comparison of your results with other schools.'''

    # Add the description to the streamlit page or to the report
    if output=='streamlit':
        st.markdown(descrip)
    elif output=='pdf':
        temp_content.append(f'<p>{descrip}</p>')

        # Then, for the PDF report, format in div and add to content list
        content.append(f'''
<div class='page'>
    <div class='section_container'>
        {''.join(temp_content)}
    </div>
</div>
''')
        return content


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


def get_chosen_result(chosen_variable, chosen_group, df, school):
    '''
    Filters the dataframe with responses to each question, to just responses
    for the chosen topic, school and group.

    Parameters
    ----------
    chosen_variable : string
        Name of the chosen topic
    chosen_group : string
        Name of the chosen group to view results by - options are
        'For all pupils', 'By year group', 'By gender', 'By FSM' or 'By SEN'
    df : dataframe
        Dataframe with responses to all the questions for all topics
    school : string
        Name of school to get results for
        
    Returns
    ----------
    chosen_result : dataframe
        Contains responses to each question in the chosen topic, with the
        results extracted so they are in seperate rows and columns (rather
        than original format where they are nested in lists)

    '''
    # Set default values
    year_group = ['All']
    gender = ['All']
    fsm = ['All']
    sen = ['All']
    group_lab = 'year_group_lab' # not used, just require default else get error

    # Depending on chosen breakdown, alter one of the above variables
    # If the chosen group was All, then no changes are made (as this is default)
    if chosen_group == 'By year group':
        year_group = ['Year 8', 'Year 10']
        group_lab = 'year_group_lab'
    elif chosen_group == 'By gender':
        gender = ['Girl', 'Boy']
                #'I describe myself in another way', 'Non-binary',
                #'Prefer not to say']
        group_lab = 'gender_lab'
    elif chosen_group == 'By FSM':
        fsm = ['FSM', 'Non-FSM']
        group_lab = 'fsm_lab'
    elif chosen_group == 'By SEN':
        sen = ['SEN', 'Non-SEN']
        group_lab = 'sen_lab'

    # Filter to chosen variable and school
    chosen = df[
        (df['group'] == chosen_variable) &
        (df['school_lab'] == school) &
        (df['year_group_lab'].isin(year_group)) &
        (df['gender_lab'].isin(gender)) &
        (df['fsm_lab'].isin(fsm)) &
        (df['sen_lab'].isin(sen))]

    # Extract the lists with results stored in the dataframe
    # e.g. ['Yes', 'No'], [20, 80], [2, 8] in the original data will become
    # seperate columns with [Yes, 20, 2] and [No, 80, 8]
    df_list = []
    for index, row in chosen.iterrows():
        # Extract results as long as it isn't NaN (e.g. NaN when n<10)
        if ~np.isnan(row.n_responses):
            df = pd.DataFrame(zip(literal_eval(row['cat'].replace('nan', 'None')),
                                literal_eval(row['cat_lab']),
                                literal_eval(row['percentage']),
                                literal_eval(row['count'])),
                            columns=['cat', 'cat_lab', 'percentage', 'count'])
            # Replace NaN with max number so stays at end of sequence
            df['cat'] = df['cat'].fillna(df['cat'].max()+1)
            # Add measure (don't need to extract as string rather than list in df)
            df['measure'] = row['measure']
            df['measure_lab'] = row['measure_lab']
            df['group'] = row[group_lab]
            df_list.append(df)
        # As we still want a bar when n<10, we create a record still but label as such
        else:
            df = row.to_frame().T[['measure', 'measure_lab']]
            df['group'] = row[group_lab]
            df['cat'] = 0
            df['cat_lab'] = 'Less than 10 responses'
            df['count'] = np.nan
            df['percentage'] = 100
            df_list.append(df)

    chosen_result = pd.concat(df_list)

    return chosen_result


def reverse_categories(df):
    '''
    Resorts dataframe so categories are in reverse order, but ensuring
    non-response is still at the end (despite it being the max value).

    Parameters:
    -----------
    df : dataframe
        Dataframe with question responses, to be resorted

    Returns:
    --------
    new_df : dataframe
        Resorted dataframe
    '''
    # Resort everything except for the pupils who did not respond 
    # (which is always the final category)
    new_df = df[df['cat'] != df['cat'].max()].sort_values(by=['cat'],
                                                          ascending=False)
    
    # Append those non-response counts back to the end
    new_df = pd.concat([new_df, df[df['cat'] == df['cat'].max()]])

    return new_df


def define_multiple_charts():
    '''
    Create a dictionary designating which topics have charts that needed to be
    seperated, and how this should be done. This is to create seperate clusters
    of charts (so there can be text describing one group of charts, then
    text describing another - e.g. when they're the same topic but have
    different sets of responses options).

    Returns
    -------
    multiple_charts : dictionary
        Dictionary where key is variable and value is dictionary with sub-groups
        of topic questions
    '''
    multiple_charts = {
        'optimism': {'optimism_future': ['optimism_future'],
                    'optimism_other': ['optimism_best', 'optimism_good', 'optimism_work']},
        'appearance': {'appearance_happy': ['appearance_happy'],
                    'appearance_feel': ['appearance_feel']},
        'physical': {'physical_days': ['physical_days'],
                    'physical_hours': ['physical_hours']},
        'places': {'places_freq': ['places_freq'],
                'places_barriers': ['places_barriers___1', 'places_barriers___2',
                                    'places_barriers___3', 'places_barriers___4',
                                    'places_barriers___5', 'places_barriers___6',
                                    'places_barriers___7', 'places_barriers___8',
                                    'places_barriers___9']},
        'talk': {'talk_yesno': ['staff_talk', 'home_talk', 'peer_talk'],
                'talk_listen': ['staff_talk_listen', 'home_talk_listen', 'peer_talk_listen'],
                'talk_helpful': ['staff_talk_helpful', 'home_talk_helpful', 'peer_talk_helpful'],
                'talk_if': ['staff_talk_if', 'home_talk_if', 'peer_talk_if']},
        'local_env': {'local_safe': ['local_safe'],
                    'local_other': ['local_support', 'local_trust',
                                    'local_neighbours', 'local_places']},
        'future': {'future_options': ['future_options'],
                'future_interest': ['future_interest'],
                'future_support': ['future_support']}
    }

    return multiple_charts


def create_bar_charts(chosen_variable, chosen_result,
                      output='streamlit', content=None):
    '''
    Creates the section of bar charts and their accompanying text, for streamlit
    page or PDF report.

    Parameters
    ----------
    chosen_variable : string
        Name of the chosen topic
    chosen_result : dataframe
        Contains responses to each question in the chosen topic, school and group
    output : string
        Specifies whether to write for 'streamlit' (default) or 'pdf'.
    content : list
        Optional input used when output=='pdf', contains HTML for report.

    Returns
    -------
    content : list
        Optional return, used when output=='pdf', contains HTML for report.
    '''
    # Import dictionary designating if there are sub-groups of charts
    multiple_charts = define_multiple_charts()

    # Import descriptions for the groups of stacked bar charts
    response_descrip = create_response_description()

    # Define which variables need to be reversed - intention was to be mostly
    # be positive to negative - but made exceptions for social media use, where
    # that ordering felt counter-intuitive - and for the sub-questions of
    # autonomy where the question meaning flips between positive and negative
    reverse = ['esteem', 'negative', 'support', 'free_like', 'local_safe',
               'local_other', 'belong_local', 'bully']

    # Create stacked bar chart with seperate charts if required
    if chosen_variable in multiple_charts:
        var_dict = multiple_charts[chosen_variable]
        for key, value in var_dict.items():

            # Add description
            if key in response_descrip.keys():
                if output=='streamlit':
                    st.markdown(response_descrip[key])
                elif output=='pdf':
                    content.append(f'<p>{response_descrip[key]}</p><br>')

            # Filter to questions in sub-group, reversing categories if required
            to_plot = chosen_result[chosen_result['measure'].isin(value)]
            if key in reverse:
                to_plot = reverse_categories(to_plot)

            # Output the plots
            if output=='streamlit':
                survey_responses(to_plot)
            elif output=='pdf':
                content = survey_responses(
                    dataset=to_plot, font_size=14,
                    output='pdf', content=content)

    # Otherwise create a single stacked bar chart
    else:

        # Add description
        if chosen_variable in response_descrip.keys():
            if output=='streamlit':
                st.markdown(response_descrip[chosen_variable])
            elif output=='pdf':
                content.append(f'<p>{response_descrip[chosen_variable]}</p><br>')

        # Reverse categories if required
        if chosen_variable in reverse:
            chosen_result = reverse_categories(chosen_result)

        # Output the plot
        if output=='streamlit':
            survey_responses(chosen_result)
        elif output=='pdf':
            content = survey_responses(
                dataset=chosen_result, font_size=14,
                output='pdf', content=content)

    if output=='pdf':
        return content