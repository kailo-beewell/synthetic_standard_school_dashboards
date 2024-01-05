'''
Helper functions for creating and processing the pupil-level data
'''
import pandas as pd

def results_by_school_and_group(data, agg_func, no_pupils):
    '''
    Aggregate results for all possible schools and groups (setting result to 0 
    or NaN if no pupils from a particular group are present).

    Parameters
    ----------
    data : pandas dataframe
        Pupil-level survey responses, with their school and demographics
    agg_func : function
        Method for aggregating the dataset
    no_pupils: pandas dataframe
        Output of agg_func() where all counts are set to 0 and other results set
        to NaN, to be used in cases where there are no pupils of a particular
        group (e.g. no FSM / SEN / Year 8)


    Returns
    -------
    result : pandas DataFramne
        Dataframe where each row has the aggregation results, along with
        the relevant school and pupil groups used in that calculation
    '''

    # Initialise list to store results
    result_list = list()

    # Define the groups that we want to aggregate by - when providing a filter,
    # the first value is the name of the category and the second is the variable
    groups = [
        'All',
        ['Year 8', 'year_group_lab'],
        ['Year 10', 'year_group_lab'],
        ['Girl', 'gender_lab'],
        ['Boy', 'gender_lab'],
        ['FSM', 'fsm_lab'],
        ['Non-FSM', 'fsm_lab'],
        ['SEN', 'sen_lab'],
        ['Non-SEN', 'sen_lab']]

    # For each of the schools (which we know will all be present at least once
    # as we base the school list on the dataset itself)
    schools = data['school_lab'].dropna().drop_duplicates().sort_values()
    for school in schools:

        # For each the groupings
        for group in groups:

            # Find results for that school. If group is not equal to all,
            # then apply additional filters
            to_agg = data[data['school_lab'] == school]
            if group != 'All':
                to_agg = to_agg[to_agg[group[1]] == group[0]]

            # If the dataframe is empty (i.e. you applied a filter but there
            # were no students matching that filter) then set to the no_pupils df.
            # Otherwise, just aggregate the data using the provided function
            if len(to_agg.index) == 0:
                res = no_pupils.copy()
            else:
                res = agg_func(to_agg)

            # Specify what school it was
            res['school_lab'] = school

            # Set each group as all, but replace the relevant one if filter used
            res['year_group_lab'] = 'All'
            res['gender_lab'] = 'All'
            res['fsm_lab'] = 'All'
            res['sen_lab'] = 'All'
            if group != 'All':
                res[group[1]] = group[0]

            # Append results to list
            result_list.append(res)

    # Combine all the results into a single dataframe
    result = pd.concat(result_list)

    return(result)