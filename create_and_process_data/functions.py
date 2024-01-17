'''
Helper functions for creating and processing the pupil-level data
'''
import numpy as np
import pandas as pd

def sum_score(df):
    '''
    Find the sum of the provided columns. If any of the required columns contain,
    NaN, it will just return NaN as the result
    Inputs:
    df - pandas DataFrame, just containing the columns you want to sum
    '''
    # Convert to numeric, find sum and return
    return(df.sum(axis=1, skipna=False))


def calculate_scores(data):
    '''
    Creates scores for each pupil in the provided dataframe, for each of the
    survey topics.

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

    # Age when moved to UK is not used as a "score" persay, but needs
    # adjusting to allow you to summarise it. We move age to centre of bucket
    # e.g. 1 year old = 1.5, 2 year old = 2.5
    # As they are in dataframe, 1 = Under 1, 2 = 1 year old, so subtract .5
    # Convert to numeric (can use sum_score()) then subtract .5
    data['birth_you_age_score'] = (
        sum_score(pd.DataFrame(data['birth_you_age'])) - 0.5)

    # Autonomy
    data['autonomy_score'] = sum_score(
        data[['autonomy_pressure', 'autonomy_express', 'autonomy_decide',
            'autonomy_told', 'autonomy_myself', 'autonomy_choice']])

    # Life satisfaction requires no changes
    data['life_satisfaction_score'] = data['life_satisfaction']

    # Optimism
    data['optimism_score'] = sum_score(
        data[['optimism_future', 'optimism_best', 'optimism_good', 'optimism_work']])

    # Psychological wellbeing
    data['wellbeing_score'] = sum_score(
        data[['wellbeing_optimistic', 'wellbeing_useful', 'wellbeing_relaxed',
            'wellbeing_problems', 'wellbeing_thinking', 'wellbeing_close',
            'wellbeing_mind']])

    # Self-esteem requires reversed scoring
    data['esteem_score'] = sum_score(
        data[['esteem_satisfied', 'esteem_qualities', 'esteem_well',
            'esteem_value', 'esteem_good']].apply(lambda x: x.map(
        {1: 4,
        2: 3,
        3: 2,
        4: 1})))

    # Stress requires numbering to start at 0
    data['stress_score'] = sum_score(
        data[['stress_control', 'stress_overcome', 'stress_confident',
            'stress_way']] - 1)

    # Appearance uses first question, excluding 'prefer not to say'
    data['appearance_score'] = data['appearance_happy'].replace(11, np.nan)

    # Negative affect requires numbering to start at 0
    data['negative_score'] = sum_score(
        data[['negative_lonely', 'negative_unhappy', 'negative_like',
            'negative_cry', 'negative_school', 'negative_worry', 'negative_sleep',
            'negative_wake', 'negative_shy', 'negative_scared']] - 1)

    # Loneliness requires reversed scoring (eg. 1 often or always becomes 5)
    data['lonely_score'] = data['lonely'].map({
        1: 5,
        2: 4,
        3: 3,
        4: 2,
        5: 1})

    # Supporting your wellbeing
    data['support_score'] = sum_score(data[['support_ways', 'support_look']])

    # Sleep is based on proportion answering 1/Yes so no change required
    data['sleep_score'] = data['sleep']

    # Physical activity multiplies days by average time per day (which is in min)
    data['physical_score'] = data['physical_days']*data['physical_hours']

    # Free time/time use is based on proportion responding almost always or often
    data['free_like_score'] = data['free_like'].map({1: 1, 2: 1,
                                                    3: 0, 4: 0, 5: 0})
        
    # Use of social media requires scores of 0-8 (rather than 1-9)
    data['media_score'] = data['media_hours'] - 1

    # Places to go and things to do is based on proportion responding several or
    # lots to the first question (second question can't be used as score)
    data['places_score'] = data['places_freq'].map({1: 0, 2: 0,
                                                    3: 1, 4: 1})

    # Talking with people about feeling down
    # If answer yes, it is the average of their listen (1-4) and helpful (1-3 but 
    # rescaled to 1-4) questions, giving a total of 1-4. If answer no, it is just
    # their answer to comfortable (1-4). The scores for staff, home and peer are
    # then summed, creating an overall score of 3-12.
    for prefix in ['staff', 'home', 'peer']:
        # Create the help/listen scores
        data[f'{prefix}_talk_listen_helpful'] = (
        data[f'{prefix}_talk_listen'] +
        data[f'{prefix}_talk_helpful'].map({1: 1, 2: 2.5, 3: 4})) / 2

        # Create score column where choosen "help/listen" or "if" depending on answer to talk
        data[f'{prefix}_talk_score'] = np.where(
            data[f'{prefix}_talk']==1,
            data[f'{prefix}_talk_listen_helpful'],
            data[f'{prefix}_talk_if'])
    # Create overall score from sum of staff, home and peer scores
    data['talk_score'] = data['staff_talk_score'] + data['home_talk_score'] + data['peer_talk_score']
    # Drop columns that were used to calculate scores
    data = data.drop(['staff_talk_listen_helpful', 'home_talk_listen_helpful', 'peer_talk_listen_helpful'], axis=1)

    # Acceptance
    data['accept_score'] = sum_score(data[['accept_staff', 'accept_home', 'accept_local', 'accept_peer']])

    # School connection
    data['school_belong_score'] = data['school_belong']

    # Relationships with staff
    data['staff_relationship_score'] = sum_score(data[['staff_interest', 'staff_believe', 'staff_best', 'staff_listen']])

    # Relationship with parents/carers
    data['home_relationship_score'] = sum_score(data[['home_interest', 'home_believe', 'home_best', 'home_listen']])

    # Home environment
    data['home_happy_score'] = data['home_happy']

    # Caring responsibilities and care experience aren't converted to scores

    # Local environment
    # First question has four responses and one "don't know" (which convert to np.nan)
    # We rescale to range from 1 to 5 to match remaining questions which have 1,2,3,4,5 as responses
    data['local_safe_rescaled'] = data['local_safe'].map({
        1: 1,
        2: 2 + 1/3,
        3: 3 + 2/3,
        4: 5,
        5: np.nan})
    data['local_env_score'] = sum_score(
        data[['local_safe_rescaled', 'local_support', 'local_trust', 'local_neighbours', 'local_places']])
    data = data.drop('local_safe_rescaled', axis=1)

    # Discrimination
    # Proportion who respond often or always / some of the time / occassionally to any of the five questions
    # They're not required to have responded to all five, just need to have given one of those responses
    # to at least one of those questions
    # Identify relevant columns
    discrim_col = ['discrim_race', 'discrim_gender', 'discrim_orientation', 'discrim_disability', 'discrim_faith']
    # Find if any of them are one of those responses
    data['discrim_score'] = (
        data[discrim_col].isin([1, 2, 3]).any(axis=1).map({True: 1, False: 0}))
    # Set to NaN if all responses were NaN
    data.loc[data[discrim_col].isnull().all(axis=1), 'discrim_score'] = np.nan

    # Belonging
    # Proportion who respond strongly agree or agree
    data['belong_local_score'] = data['belong_local'].map({1: 1, 2: 1,
                                                        3: 0, 4: 0})

    # Relative wealth
    # Proportion who feel about the same as friends, excluding "don't know"
    data['wealth_score'] = data['wealth'].map({1: 0, 2: 1, 3: 0, 4: np.nan})

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
    # Proportion responding often or sometimes
    data['climate_score'] = data['climate'].map({1: 1, 2: 1, 3: 0, 4: 0})

    # Friendships and social support
    data['social_score'] = sum_score(data[['social_along', 'social_time', 'social_support', 'social_hard']])

    # Bullying
    data['bully_score'] = sum_score(data[['bully_physical', 'bully_other', 'bully_cyber']])

    return (data)

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