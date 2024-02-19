'''
Helper functions for the explore_results() section of dashboard and PDF report.
'''
import pandas as pd
import numpy as np
import streamlit as st
from markdown import markdown
from utilities.bar_charts_text import create_response_description
from utilities.bar_charts import survey_responses, details_ordered_bar
from utilities.summary_rag import result_box
from utilities.reshape_data import filter_by_group, extract_nested_results
from utilities.score_descriptions import score_descriptions


def write_page_title(output='streamlit'):
    '''
    Writes the title of this page/section (Explore Results), for the streamlit
    page or for the PDF report.

    Parameters
    ----------
    output : string
        Specifies whether to write for 'streamlit' (default) or 'pdf'.

    Returns
    -------
    html_string : string
        Optional return, used when output=='pdf', contains HTML for report.
    '''
    # Title
    title = 'Explore results'
    if output == 'streamlit':
        st.title(title)
    elif output == 'pdf':
        temp_content = []
        temp_content.append(f'''
<h1 style='page-break-before:always;' id='explore_results'>{title}</h1>''')

    # Generate the description (with some changes to the text and spacing
    # between streamlit and the PDF report)
    if output == 'streamlit':
        type1 = 'page'
        type2 = 'page'
        line_break = ''
    elif output == 'pdf':
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
    if output == 'streamlit':
        st.markdown(descrip)
    elif output == 'pdf':
        temp_content.append(f'<p>{descrip}</p>')

        # Then, for the PDF report, format in div and add to content list
        html_string = f'''
<div class='page'>
    <div class='section_container'>
        {''.join(temp_content)}
    </div>
</div>
'''
        return html_string


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
        Dataframe containing the 'variable' and 'description' columns for each
        topic.
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
    if output == 'streamlit':
        st.markdown(f'''<h2 style='font-size:55px; text-align:center;'>{
            chosen_variable_lab}</h2>''', unsafe_allow_html=True)
    elif output == 'pdf':
        content.append(f'''
<h1 style='text-align:center; page-break-before:always;'
id='{chosen_variable}'>{chosen_variable_lab}</h1>''')

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
    if output == 'streamlit':
        st.markdown(topic_descrip, unsafe_allow_html=True)
    elif output == 'pdf':
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
    if output == 'streamlit':
        st.subheader(header)
    elif output == 'pdf':
        content.append(f'<h3>{header}</h3>')

    # Section description
    section_descrip = f'''
In this section, you can see how pupils at you school responded to survey
questions that relate to the topic of '{chosen_variable_lab.lower()}'.'''
    if output == 'streamlit':
        st.markdown(section_descrip)
    elif output == 'pdf':
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
    # Filter by the specified school and grouping
    chosen, group_lab = filter_by_group(df=df, chosen_group=chosen_group,
                                        output='explore', chosen_school=school)

    # Filter by the chosen variable
    chosen = chosen[chosen['group'] == chosen_variable]

    # Extract the nested lists in the dataframe
    chosen_result = extract_nested_results(chosen, group_lab)

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
        Dictionary where key is variable and value is dictionary with
        sub-groups of topic questions
    '''
    multiple_charts = {
        'optimism': {'optimism_future': ['optimism_future'],
                     'optimism_other': ['optimism_best',
                                        'optimism_good',
                                        'optimism_work']},
        'appearance': {'appearance_happy': ['appearance_happy'],
                       'appearance_feel': ['appearance_feel']},
        'physical': {'physical_days': ['physical_days'],
                     'physical_hours': ['physical_hours']},
        'places': {'places_freq': ['places_freq'],
                   'places_barriers': ['places_barriers___1',
                                       'places_barriers___2',
                                       'places_barriers___3',
                                       'places_barriers___4',
                                       'places_barriers___5',
                                       'places_barriers___6',
                                       'places_barriers___7',
                                       'places_barriers___8',
                                       'places_barriers___9']},
        'talk': {'talk_yesno': ['staff_talk',
                                'home_talk',
                                'peer_talk'],
                 'talk_listen': ['staff_talk_listen',
                                 'home_talk_listen',
                                 'peer_talk_listen'],
                 'talk_helpful': ['staff_talk_helpful',
                                  'home_talk_helpful',
                                  'peer_talk_helpful'],
                 'talk_if': ['staff_talk_if',
                             'home_talk_if',
                             'peer_talk_if']},
        'local_env': {'local_safe': ['local_safe'],
                      'local_other': ['local_support',
                                      'local_trust',
                                      'local_neighbours',
                                      'local_places']},
        'future': {'future_options': ['future_options'],
                   'future_interest': ['future_interest'],
                   'future_support': ['future_support']}
    }

    return multiple_charts


def create_bar_charts(chosen_variable, chosen_result,
                      output='streamlit', content=None):
    '''
    Creates the section of bar charts and their accompanying text, for
    streamlit page or PDF report.

    Parameters
    ----------
    chosen_variable : string
        Name of the chosen topic
    chosen_result : dataframe
        Contains responses to each question in the chosen topic, school + group
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

    # Create stacked bar chart with seperate chart groups if required
    if chosen_variable in multiple_charts:
        # Counter as we don't want to break page before first description,
        # but do for the later description
        i = -1
        var_dict = multiple_charts[chosen_variable]
        for key, value in var_dict.items():
            i += 1
            # Add description
            if key in response_descrip.keys():
                if output == 'streamlit':
                    st.markdown(response_descrip[key])
                elif output == 'pdf':
                    # Break page before description, unless it's the first.
                    if i > 0:
                        content.append(f'''
<p style='page-break-before:always;'>{response_descrip[key]}</p>''')
                    else:
                        content.append(f'<p>{response_descrip[key]}</p>')

            # Filter to questions in sub-group, reversing categories if need to
            to_plot = chosen_result[chosen_result['measure'].isin(value)]
            if key in reverse:
                to_plot = reverse_categories(to_plot)

            # Output the plots
            if output == 'streamlit':
                survey_responses(to_plot)
            elif output == 'pdf':
                content = survey_responses(
                    dataset=to_plot, font_size=14,
                    output='pdf', content=content)

    # Otherwise create a single stacked bar chart
    else:

        # Add description
        if chosen_variable in response_descrip.keys():
            if output == 'streamlit':
                st.markdown(response_descrip[chosen_variable])
            elif output == 'pdf':
                content.append(
                    f'<p>{response_descrip[chosen_variable]}</p>')

        # Reverse categories if required
        if chosen_variable in reverse:
            chosen_result = reverse_categories(chosen_result)

        # Output the plot
        if output == 'streamlit':
            survey_responses(chosen_result)
        elif output == 'pdf':
            content = survey_responses(
                dataset=chosen_result, font_size=14,
                output='pdf', content=content)

    if output == 'pdf':
        return content


def write_comparison_intro(
        chosen_variable, chosen_variable_lab, score_descriptions,
        output='streamlit', content=None):
    '''
    Write the introduction to the comparison section (heading, description
    and RAG rating)

    Parameters
    ----------
    chosen_variable : string
        Chosen variable (e.g. 'autonomy')
    chosen_variable_lab : string
        Label for the chosen variable (e.g. 'Autonomy')
    score_descriptions : dictionary
        Dictionary with variable and then the appropriate descriptions for this
        section (range of score, and interpretation of score)
    output : string
        Specifies whether to write for 'streamlit' (default) or 'pdf'.
    content : list
        Optional input used when output=='pdf', contains HTML for report.

    Returns
    -------
    content : list
        Optional return, used when output=='pdf', contains HTML for report.
    '''
    # Heading
    heading = 'Comparison with other schools'
    if output == 'streamlit':
        st.subheader(heading)
    elif output == 'pdf':
        content.append(f'''
<h3 style='page-break-before: always;'>{heading}</h3>''')

    # Description text
    description = f'''
In this section, an overall score for the topic of
'{chosen_variable_lab.lower()}' has been calculated for each pupil with
complete responses on this question. Possible scores for each pupil on this
topic range from {score_descriptions[chosen_variable][0]} with
**higher scores indicating {score_descriptions[chosen_variable][1]}** -
and vice versa for lower scores. The mean score of the pupils at you
school is compared with pupils who completed the same survey questions at other
schools. This allows you to see whether the typical score for pupils at your
school is average, below average or above average.'''

    # Add description to dashboard or report
    if output == 'streamlit':
        st.markdown(description)
    elif output == 'pdf':
        content.append(markdown(description))
        return content


def write_comparison_result(chosen_school, between_schools, group,
                            output='streamlit', content=None):
    '''
    Write the introduction to the comparison section (heading, description
    and RAG rating)

    Parameters
    ----------
    chosen_school : string
        Name of chosen school
    between_schools: dataframe
        Dataframe with scores for the chosen variable in each school
    output : string
        Specifies whether to write for 'streamlit' (default) or 'pdf'.
    content : list
        Optional input used when output=='pdf', contains HTML for report.
    group : string
        Pupil group

    Returns
    -------
    content : list
        Optional return, used when output=='pdf', contains HTML for report.
    '''
    # Provide title, unless looking at all pupils, in which case drop group too
    if group != 'All':
        description = f'''**{group}**

'''
    else:
        group = ''
        description = ''

    # Get number of responses at school
    school_mean = between_schools.loc[
        between_schools['school_lab'] == chosen_school, 'mean'].to_list()[0]

    # Display message if it was less than 10 (and so NaN)
    if np.isnan(school_mean):
        description += '''
There were less than ten complete responses from these pupils at your school,
so the results are not shown.
'''
    # Otherwise...
    else:
        # Get count of pupils who completed the topic questions
        topic_count = int(between_schools.loc[
            between_schools['school_lab'] == chosen_school,
            'count'].to_list()[0])

        # Get total responses and total schools (can just take first item as
        # whole column will be the same value for each school)
        total_responses = str(int(
            between_schools['total_pupils'].to_list()[0]))
        total_schools = str(int(
            between_schools['group_n'].to_list()[0]))
        description += f'''
Your school had {topic_count} complete responses. Across
Northern Devon, there were {total_responses} complete responses from
{total_schools} schools. The average score for the pupils at your school,
compared to other schools in Northern Devon, was:'''

    # Add description to page
    if output == 'streamlit':
        st.markdown(description)
    elif output == 'pdf':
        content.append(markdown(description))

    # If school wasn't NaN...
    if not np.isnan(school_mean):
        # Get RAG rating
        devon_rag = between_schools.loc[
            between_schools['school_lab'] == chosen_school, 'rag'].to_list()[0]
        # Drop any schools that were NaN (i.e. n<10)
        between_schools = between_schools[between_schools['mean'].notna()]
        # Add the RAG result and ordered bar chart
        if output == 'streamlit':
            result_box(devon_rag)
            details_ordered_bar(between_schools, chosen_school)
        elif output == 'pdf':
            content.append(result_box(devon_rag, 'pdf'))
            content = details_ordered_bar(
                school_scores=between_schools, school_name=chosen_school,
                font_size=16, output='pdf', content=content)

    if output == 'pdf':
        return content


def create_explore_topic_page(
        chosen_variable_lab, topic_dict, df_scores, chosen_school,
        chosen_group, df_prop, content):
    '''
    Add an explore results page with responses to a given topic to report HTML.

    Parameters
    ----------
    chosen_variable_lab : string
        Chosen variable in label format (e.g. 'Psychological wellbeing')
    topic_dict : dictionary
        Dictionary of topics where key is variable_lab and value is variable
    df_scores : dataframe
        Dataframe with scores for each topic
    chosen_school : string
        Name of the chosen school
    chosen_group : string
        Name of the chosen group to view results by - options are
        'For all pupils', 'By year group', 'By gender', 'By FSM' or 'By SEN'
    df_prop : dataframe
        Dataframe with the proportion of pupils providing each response to each
        survey question
    content : list
        Optional input used when output=='pdf', contains HTML for report.

    Returns
    -------
    content : list
        Optional return, used when output=='pdf', contains HTML for report.
    '''
    # Convert from variable_lab to variable
    chosen_variable = topic_dict[chosen_variable_lab]

    # Topic header and description
    content = write_topic_intro(chosen_variable, chosen_variable_lab,
                                df_scores, output='pdf', content=content)

    # Section header and description
    content = write_response_section_intro(
        chosen_variable_lab, output='pdf', content=content)

    # Get dataframe with results for the chosen variable, group and school
    chosen_result = get_chosen_result(
        chosen_variable, chosen_group, df_prop, chosen_school)

    # Produce bar charts, plus their chart section descriptions and titles
    content = create_bar_charts(
        chosen_variable, chosen_result, output='pdf', content=content)

    # Create dataframe based on chosen variable
    between_schools, group_lab, order = filter_by_group(
        df=df_scores, chosen_group=chosen_group, output='compare',
        chosen_variable=chosen_variable+'_score')

    # Write the comparison intro text
    content = write_comparison_intro(
        chosen_variable, chosen_variable_lab, score_descriptions,
        output='pdf', content=content)

    # Filter to each group (will just be 'all' if was for all pupils), then
    # print the results and create the ordered bar chart for each
    for group in order:
        temp_content = []
        # Filter to group and get result
        group_result = between_schools[between_schools[group_lab] == group]
        temp_content = write_comparison_result(
            chosen_school, group_result, group, output='pdf',
            content=temp_content)
        # Insert temp_content into a div class and add to content
        content.append(f'''
    <div class='responses_container'>
        {''.join(temp_content)}
    </div>''')

    return content
