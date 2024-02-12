'''
Helper functions for reshaping data or extracting a certain element from the
data, often used across multiple different pages
'''


def filter_by_group(df, chosen_group, chosen_school, output):
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
    chosen_school : string
        Name of the school to filter results for
    output : string
        Defines where data will be used - either 'explore' or 'summary'

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

    # Filter to chosen variable and school
    chosen = df[
        (df['school_lab'] == chosen_school) &
        (df['year_group_lab'].isin(year_group)) &
        (df['gender_lab'].isin(gender)) &
        (df['fsm_lab'].isin(fsm)) &
        (df['sen_lab'].isin(sen))]

    # Return the relevant results for the given output
    if output == 'explore':
        return chosen, group_lab
    elif output == 'summary':
        return chosen, group_lab, order


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
