'''
Helper functions for creating and processing the pupil-level data
'''
import numpy as np
import pandas as pd
import re


def sum_score(df):
    '''
    Find the sum of the provided columns. If any of the required columns
    contain, NaN, it will just return NaN as the result

    Parameters
    ----------
    df : pandas DataFrame
        Dataframe just containing the columns you want to sum
    '''
    # Convert to numeric, find sum and return
    return df.sum(axis=1, skipna=False)


def reverse_score(scores, min, max):
    '''
    Reverse scores in the provided array, based on the known min and max of the
    scale of the scores. NaN will remain as NaN.

    Parameters
    ----------
    scores : array
        Array with scores to be reversed
    min : int
        Minimum possible score
    max : int
        Maximum possible score


    Returns
    -------
    Array with scores reversed
    '''
    return [max + min - x for x in scores]


def calculate_scores(data):
    '''
    Creates scores for each pupil in the provided dataframe, for each of the
    survey topics. Note, when referring to where scores are "set to positive"
    or "in a positive direction" or a "negative directioN", this refers to
    whether the maximum score is a positive or negative outcome.

    Parameters
    ----------
    data : pandas dataframe
        Pupil-level survey responses

    Returns
    -------
    data : pandas dataframe
        Pupil-level survey responses with the addition of topic scores
    '''
    # Gender, transgender, sexual orientation, neurodivergence, and yes/no
    # of whether born in UK are not converted to scores

    # Autonomy
    # Reverse score on two questions in negative direction
    data['autonomy_pressure_rev'] = reverse_score(
        data['autonomy_pressure'], min=1, max=5)
    data['autonomy_told_rev'] = reverse_score(
        data['autonomy_told'], min=1, max=5)
    # Sum questions
    data['autonomy_score'] = sum_score(
        data[['autonomy_pressure_rev',
              'autonomy_express',
              'autonomy_decide',
              'autonomy_told_rev',
              'autonomy_myself',
              'autonomy_choice']])
    # Drop the temporary columns created to support score calculation
    data = data.drop(['autonomy_pressure_rev', 'autonomy_told_rev'], axis=1)

    # Life satisfaction requires no changes
    data['life_satisfaction_score'] = data['life_satisfaction']

    # Optimism
    data['optimism_score'] = sum_score(
        data[['optimism_future', 'optimism_best', 'optimism_good',
              'optimism_work']])

    # Psychological wellbeing
    data['wellbeing_score'] = sum_score(
        data[['wellbeing_optimistic', 'wellbeing_useful', 'wellbeing_relaxed',
              'wellbeing_problems', 'wellbeing_thinking', 'wellbeing_close',
              'wellbeing_mind']])

    # Self-esteem requires reversed scoring
    data['esteem_score'] = sum_score(
        data[['esteem_satisfied', 'esteem_qualities', 'esteem_well',
              'esteem_value', 'esteem_good']].apply(
                lambda x: reverse_score(x, min=1, max=4)))

    # Stress
    # First, I calculate score as in GM - that was a negative direction, so
    # we have to change the two positive direction options to the negative
    data['stress_confident_rev'] = reverse_score(
        data['stress_confident'], min=1, max=5)
    data['stress_way_rev'] = reverse_score(data['stress_way'], min=1, max=5)
    data['stress_score'] = sum_score(
        data[['stress_control', 'stress_overcome', 'stress_confident_rev',
              'stress_way_rev']] - 1)
    # Drop the temporary columns created to support score calculation
    data = data.drop(['stress_confident_rev', 'stress_way_rev'], axis=1)
    # We are setting all scores to positive - so reverse the final score
    data['stress_score'] = reverse_score(data['stress_score'], min=0, max=16)

    # Appearance uses first question, excluding 'prefer not to say'
    data['appearance_score'] = data['appearance_happy'].replace(11, np.nan)

    # Negative affect requires numbering to start at 0
    data['negative_score'] = sum_score(
        data[['negative_lonely', 'negative_unhappy', 'negative_like',
              'negative_cry', 'negative_school', 'negative_worry',
              'negative_sleep', 'negative_wake', 'negative_shy',
              'negative_scared']] - 1)
    # We are setting all scores to positive - so reverse the final score
    data['negative_score'] = reverse_score(
        data['negative_score'], min=0, max=20)

    # Loneliness requires reversed scoring (eg. 1 often or always becomes 5)
    # to match GM - but we are setting all scores to positive - so leave as is
    data['lonely_score'] = data['lonely']

    # Supporting your wellbeing - reversed so its in the positive direction
    data['support_score'] = sum_score(data[['support_ways', 'support_look']])
    data['support_score'] = reverse_score(data['support_score'], min=2, max=8)

    # Sleep is based on proportion answering 1/Yes so no change required
    data['sleep_score'] = data['sleep']

    # Physical activity multiplies days by avg time per day (which is in min)
    data['physical_score'] = data['physical_days']*data['physical_hours']

    # Free time/time use - reversed so its in the positive direction
    data['free_like_score'] = reverse_score(data['free_like'], min=1, max=5)

    # Use of social media requires scores of 0-8 (rather than 1-9)
    # Then we reverse it so it's in the positive direction
    data['media_score'] = data['media_hours'] - 1
    data['media_score'] = reverse_score(data['media_score'], min=0, max=8)

    # Places to go and things to do (unchanged as that is simplest)
    data['places_score'] = data['places_freq']

    # Talking with people about feeling down
    # If answer yes, it is the average of their listen (1-4) and helpful (1-3
    # but rescaled to 1-4) questions, giving a total of 1-4. If answer no, it
    # is just their answer to comfortable (1-4). The scores for staff, home and
    # peer are then summed, creating an overall score of 3-12.
    for prefix in ['staff', 'home', 'peer']:
        # Create the help/listen scores (see it takes the average through /2)
        data[f'{prefix}_talk_listen_helpful'] = (
            data[f'{prefix}_talk_listen'] +
            data[f'{prefix}_talk_helpful'].map({1: 1, 2: 2.5, 3: 4})) / 2
        # Create score column where choosen "help/listen" or "if" depending on
        # answer to talk
        data[f'{prefix}_talk_score'] = np.where(
            data[f'{prefix}_talk'] == 1,
            data[f'{prefix}_talk_listen_helpful'],
            data[f'{prefix}_talk_if'])
    # Create overall score from sum of staff, home and peer scores
    data['talk_score'] = (data['staff_talk_score'] +
                          data['home_talk_score'] +
                          data['peer_talk_score'])
    # Drop columns that were used to calculate scores
    data = data.drop(['staff_talk_listen_helpful',
                      'home_talk_listen_helpful',
                      'peer_talk_listen_helpful'], axis=1)

    # Acceptance
    data['accept_score'] = sum_score(
        data[['accept_staff', 'accept_home', 'accept_local', 'accept_peer']])

    # School connection
    data['school_belong_score'] = data['school_belong']

    # Relationships with staff
    data['staff_relationship_score'] = sum_score(
        data[['staff_interest', 'staff_believe',
              'staff_best', 'staff_listen']])

    # Relationship with parents/carers
    data['home_relationship_score'] = sum_score(
        data[['home_interest', 'home_believe', 'home_best', 'home_listen']])

    # Home environment
    data['home_happy_score'] = data['home_happy']

    # Caring responsibilities and care experience aren't converted to scores

    # Local environment
    # First question has four responses and one "don't know" (which convert to
    # np.nan). We rescale to range from 1 to 5 to match remaining questions
    # which have 1,2,3,4,5 as responses
    data['local_safe_rescaled'] = data['local_safe'].map({
        1: 1,
        2: 2 + 1/3,
        3: 3 + 2/3,
        4: 5,
        5: np.nan})
    data['local_env_score'] = sum_score(
        data[['local_safe_rescaled', 'local_support', 'local_trust',
              'local_neighbours', 'local_places']])
    data = data.drop('local_safe_rescaled', axis=1)
    # We then reverse the score so it is in the positive direction
    data['local_env_score'] = reverse_score(
        data['local_env_score'], min=5, max=25)

    # Discrimination
    # Proportion who respond often or always / some of the time / occassionally
    # to any of the five questions. They're not required to have responded to
    # all five, just need to have given one of those responses to at least one
    # of those questions.
    # Identify relevant columns
    discrim_col = ['discrim_race', 'discrim_gender', 'discrim_orientation',
                   'discrim_disability', 'discrim_faith']
    # Find if any of them are one of those responses
    # If true, set to 1. If false, set to 2. This is because true is the
    # negative outcome whilst false is the positive outcome (so set to higher
    # score). We use 1 and 2 rather than 0 and 1 as often the score for a
    # school will fall fairly low in the synthetic data, and when 0 is the
    # minimum, the minimum bar doesn't show on the plot and there's no x axis
    # ticks to explain
    data['discrim_score'] = (
        data[discrim_col].isin([1, 2, 3]).any(axis=1).map({True: 1, False: 2}))
    # Set to NaN if all responses were NaN
    data.loc[data[discrim_col].isnull().all(axis=1), 'discrim_score'] = np.nan

    # Belonging - reverse so its in the positive direction
    data['belong_local_score'] = reverse_score(
        data['belong_local'], min=1, max=4)

    # Relative wealth
    # Proportion who feel about the same as friends, excluding "don't know"
    data['wealth_score'] = data['wealth'].map({1: 0, 2: 0, 3: 1, 4: np.nan})

    # Work, education and training opportunities
    # Rescale future options so 1-5 (matching future interest and support)
    # For all, setting the "unsure" option to np.nan
    data['future_score'] = (
        data['future_options'].map({
            1: 1,
            2: 2.5,
            3: 4,
            4: np.nan}) +
        data['future_interest'].replace(5, np.nan) +
        data['future_support'].replace(5, np.nan)
    )

    # Climate change
    data['climate_score'] = data['climate']

    # Friendships and social support
    data['social_score'] = sum_score(data[['social_along', 'social_time',
                                           'social_support', 'social_hard']])

    # Bullying
    data['bully_score'] = sum_score(data[['bully_physical', 'bully_other',
                                          'bully_cyber']])
    # Reverse so it's in the positive direction
    data['bully_score'] = reverse_score(data['bully_score'], min=3, max=12)

    return (data)


def results_by_school_and_group(
        data, agg_func, no_pupils, response_col=None, labels=None):
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
        Output of agg_func() where all counts are set to 0 and other results
        set to NaN, to be used in cases where there are no pupils of a
        particular group (e.g. no FSM / SEN / Year 8)
    response_col : list
        Optional argument used when agg_func is aggregate_proportions(). It is
        the list of columns that we want to aggregate.
    labels : dictionary
        Optional argument used when agg_func is aggregate_proportions(). It is
        a dictionary with all possible questions as keys, then values are
        another dictionary where keys are all the possible numeric (or nan)
        answers to the question, and values are relevant label for each answer.

    Returns
    -------
    result : pandas DataFrame
        Dataframe where each row has the aggregation results, along with
        the relevant school and pupil groups used in that calculation
    '''

    # Initialise list to store results
    result_list = list()

    # Define the groups that we want to aggregate by - when providing a filter,
    # first value is the name of the category and the second is the variable
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
            # were no students matching that filter) then set to the no_pupils
            # df. Otherwise, aggregate the data using the provided function
            if len(to_agg.index) == 0:
                res = no_pupils.copy()
            else:
                if response_col is None:
                    res = agg_func(to_agg)
                else:
                    res = agg_func(
                        data=to_agg, response_col=response_col, labels=labels)

            # Specify what school it was
            res['school_lab'] = school

            # Set each group as all, replacing one if filter used
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

    return result


def convert_boolean(true_list, false_list, mask):
    '''
    Conditionally replace values of boolean list from one list when True and
    another when False.

    Parameters
    ----------
    true_list : list
        Contains values to use if True
    false_list : list
        Contains values to use if False
    mask : list
        Boolean list
    '''
    iter_true = iter(true_list)
    iter_false = iter(false_list)
    return [next(iter_true) if item else next(iter_false) for item in mask]


def aggregate_proportions(data, response_col, labels, hide_low_response=False):
    '''
    Aggregates each of the columns provided by response_col, for the chosen
    dataset.

    This function uses the known possible values for each column, it counts
    occurences of each (inc. number missing) and makes the answer as a single
    dataframe row, where counts and percentages and categories are stored as
    lists within cells of that row. The function returns a dataframe containing
    all of those rows. It is designed to based on all possible values rather
    than only on values present - else e.g. if no-one responded 3, you could
    have a function that just returns counts of responses to 1, 2 and 4, which
    would then create issues when we try and plot the data.

    For the branching question (talking about feelings), the value counts are
    calculated from a subset of the data (as the no response should only be
    from those who branched onto that question, and not those who branched onto
    the other question (or never answered the first branching question)).

    Parameters
    ----------
    data : dataframe
        Dataframe with rows for each pupil and including all the response_col
    response_col : list
        List of columns that we want to aggregate
    labels : dictionary
        Dictionary with all possible questions as keys, then values are another
        dictionary where keys are all the possible numeric (or nan) answers to
        the question, and values are the relevant label for each answer.
    hide_low_response : boolean
        Whether to hide responses when a response option gets less than 10
        responses (rather than norm elsewhere, which is just requiring 10
        responses to the entire item rather than to each response option)

    Returns
    -------
    pd.concat(rows): dataframe
        Dataframe with the aggregate responses to each of the response_col
    '''
    # Initialise list to store rows of the dataframe
    rows = list()

    # Loop through the columns of interest
    for col_lab in response_col:

        # Find the name of the numeric version of the column
        col = col_lab.replace('_lab', '')

        # Identify if column is branching from "yes" to talking with someone
        if any([substring in col for substring in ['talk_listen',
                                                   'talk_helpful']]):
            # Get the prefix (staff, home or peer)
            prefix = re.sub('_talk_listen|_talk_helpful', '', col)
            # Filter the data to only those who said they talked with them
            # (branch)
            data_subset = data[data[f'{prefix}_talk'] == 1]
            # Find value counts
            value_counts = data_subset[col].value_counts(dropna=False)

        # Identify if the column is branching from "no" to talking with someone
        elif 'talk_if' in col:
            # Get the prefix (staff, home or peer)
            prefix = re.sub('_talk_if', '', col)
            # Filter the data to only those who said they didn't talk to them
            # (branch)
            data_subset = data[data[f'{prefix}_talk'] == 0]
            # Find value counts
            value_counts = data_subset[col].value_counts(dropna=False)

        # For any other columns, no subsetting of the data is required
        else:
            # Find value counts
            value_counts = data[col].value_counts(dropna=False)

        # Get all possible category values and labels from dictionary
        cat = list(labels[col].keys())
        cat_lab = list(labels[col].values())

        # Initalise list for storing counts
        counts = []
        # For each of the possible values in labels - if the value was present,
        # extract from the counts series, but if not, set count to 0
        for value in labels[col].keys():
            if value in value_counts.index:
                counts.append(value_counts[value])
            else:
                counts.append(0)

        # Convert list of counts to list of percentages, and create rounded
        # version
        percentages = [(x/sum(counts))*100 for x in counts]

        # If True to hide when individual response options are n<10
        if hide_low_response:
            # Create mask which is TRUE when responses where n>=10 (ignoring
            # final option (non-response) which we don't mind being n<10)
            mask = [x >= 10 for x in counts[:-1]]

            # If all >=10, keep non-response
            if all(mask):
                mask += [True]
            # If any option is <10, also hide non-response (else could deduce)
            else:
                mask += [False]

            # Use mask to set values to NaN
            counts = convert_boolean(
                counts, np.full(len(counts), np.nan), mask)
            percentages = convert_boolean(
                percentages, np.full(len(percentages), np.nan), mask)

        # Create dataframe row using the calculated data
        # Use np.nansum() so it ignores NaN when calculating sum
        df_row = pd.DataFrame({
            'cat': [cat],
            'cat_lab': [cat_lab],
            'count': [counts],
            'percentage': [percentages],
            'measure': col,
            'n_responses': np.nansum(counts)
        })
        # Append to list
        rows.append(df_row)

    # Combine into a single dataframe and return
    return pd.concat(rows)
