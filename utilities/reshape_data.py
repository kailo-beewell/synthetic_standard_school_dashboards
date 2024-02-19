'''
Helper functions for reshaping data or extracting a certain element from the
data, often used across multiple different pages
'''
import pandas as pd
from ast import literal_eval
import numpy as np


def filter_by_group(df, chosen_group, output,
                    chosen_school=None, chosen_variable=None):
    '''
    Filter dataframe so just contains rows relevant for chosen group (either
    results from all pupils, or from the two chosen groups) and school

    Parameters
    ----------
    df : dataframe
        Dataframe to be filtered
    chosen_group : string
        The group for results to be viewed by - one of: 'For all pupils',
        'By year group', 'By gender', 'By FSM', or 'By SEN'
    output : string
        Defines where data will be used - either 'explore' or 'summary'
    chosen_school : string
        Optional input, name of a school to filter to as well
    chosen_variable : string
        Optional input, name of a variable to filter to as well

    Returns
    -------
    Depends on chosen output
    '''
    # Set default values
    year_group = ['All']
    gender = ['All']
    fsm = ['All']
    sen = ['All']

    # These are default values that each page will need to avoid errors
    # (explore uses it - it could use any of them - and summary doesn't)
    if output == 'explore':
        group_lab = 'year_group_lab'
    elif output == 'summary':
        group_lab = None
        order = None
    elif output == 'compare':
        group_lab = 'year_group_lab'
        order = ['All']

    # Depending on chosen breakdown, alter one of the above variables
    # If the chosen group was All, then no changes are made, as this is default
    if chosen_group == 'By year group':
        group_lab = 'year_group_lab'
        year_group = ['Year 8', 'Year 10']
        order = ['Year 8', 'Year 10']
    elif chosen_group == 'By gender':
        group_lab = 'gender_lab'
        gender = ['Girl', 'Boy']
        order = ['Girl', 'Boy']
    elif chosen_group == 'By FSM':
        group_lab = 'fsm_lab'
        fsm = ['FSM', 'Non-FSM']
        order = ['FSM', 'Non-FSM']
    elif chosen_group == 'By SEN':
        group_lab = 'sen_lab'
        sen = ['SEN', 'Non-SEN']
        order = ['SEN', 'Non-SEN']

    # Filter to chosen group
    chosen = df[
        (df['year_group_lab'].isin(year_group)) &
        (df['gender_lab'].isin(gender)) &
        (df['fsm_lab'].isin(fsm)) &
        (df['sen_lab'].isin(sen))]

    # Filter to chosen school, if relevant
    if chosen_school is not None:
        chosen = chosen[chosen['school_lab'] == chosen_school]

    # Filter to chosen variable, if relevant
    if chosen_variable is not None:
        chosen = chosen[chosen['variable'] == chosen_variable]

    # Return the relevant results for the given output
    if output == 'explore':
        return chosen, group_lab
    elif output == 'summary':
        return chosen, group_lab, order
    elif output == 'compare':
        return chosen, group_lab, order


def extract_nested_results(chosen, group_lab, plot_group=False):
    '''
    Extract lists of results that were stored in dataframe.
    e.g. ['Yes', 'No'], [20, 80], [2, 8] in the original data will become
    seperate columns with [Yes, 20, 2] and [No, 80, 8]

    Parameters
    ----------
    chosen : dataframe
        Dataframe with the nested lists to be extracted
    group_lab : string
        Name of chosen group (e.g. gender_lab, fsm_lab)
    '''
    # Initalise empty list to store rows
    df_list = []

    # Loop through each of the rows in the dataframe
    for index, row in chosen.iterrows():

        # Extract results as long as it isn't NaN (e.g. NaN when n<10)
        if ~np.isnan(row.n_responses):
            # Literal_eval means the string lists become actual lists
            df = pd.DataFrame(
                zip(literal_eval(row['cat'].replace('nan', 'None')),
                    literal_eval(row['cat_lab']),
                    literal_eval(row['percentage'].replace('nan', 'None')),
                    literal_eval(row['count'].replace('nan', 'None'))),
                columns=['cat', 'cat_lab', 'percentage', 'count'])
            # Replace NaN with max number so stays at end of sequence
            df['cat'] = df['cat'].fillna(df['cat'].max()+1)
            # Add the string columns (no extraction needed)
            df['measure'] = row['measure']
            df['measure_lab'] = row['measure_lab']
            df['group'] = row[group_lab]
            if plot_group:
                df['plot_group'] = row['plot_group']
            df_list.append(df)

        # As we still want a bar when n<10, we create a record still but label
        # it to indicate n<10
        else:
            df = row.to_frame().T[['measure', 'measure_lab']]
            df['group'] = row[group_lab]
            if plot_group:
                df['plot_group'] = row['plot_group']
            df['cat'] = 0
            df['cat_lab'] = 'Less than 10 responses'
            df['count'] = np.nan
            df['percentage'] = 100
            df_list.append(df)

    # Combine into a single dataframe
    chosen_result = pd.concat(df_list)

    return chosen_result


def get_school_size(counts, school):
    '''
    Get the total pupil number for a given school

    Parameters
    ----------
    counts : dataframe
        Dataframe containing the count of pupils at each school
    school : string
        Name of the school

    Returns
    -------
    school_size : integer
        Total number of pupils at school (who answered at least one question)
    '''
    # Filter to relevant school
    school_counts = counts.loc[counts['school_lab'] == school]

    # Find total school size
    school_size = school_counts.loc[
        (school_counts['year_group_lab'] == 'All') &
        (school_counts['gender_lab'] == 'All') &
        (school_counts['fsm_lab'] == 'All') &
        (school_counts['sen_lab'] == 'All'), 'count'].values[0].astype(int)

    return school_size
