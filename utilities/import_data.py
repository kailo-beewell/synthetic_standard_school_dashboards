'''
Helper function for importing the data from TiDB Cloud
'''
import numpy as np
import pandas as pd
import streamlit as st
from pandas.testing import assert_frame_equal

def import_tidb_data(tests=False):
    '''
    Imports all the datasets from TiDB Cloud, fixes any data type issues, and
    saves the datasets to the session state.

    Parameters
    ----------
    tests : Boolean
        Whether to run tests to check the data imported from TiDB cloud matches
        the CSV files in the GitHub repository
    '''
    # Set up connection
    conn = st.connection('tidb', type='sql')

    # Scores
    if 'scores' not in st.session_state:
        scores = conn.query('SELECT * FROM aggregate_scores;')
        st.session_state['scores'] = scores

    # Scores RAG
    if 'scores_rag' not in st.session_state:
        scores_rag = conn.query('SELECT * FROM aggregate_scores_rag;')
        # Convert columns to numric
        to_fix = ['mean', 'count', 'total_pupils', 'group_n', 
                'group_wt_mean', 'group_wt_std', 'lower', 'upper']
        for col in to_fix:
            scores_rag[col] = pd.to_numeric(scores_rag[col], errors='ignore')
        # Convert string 'nan' to actual np.nan
        scores_rag['rag'] = scores_rag['rag'].replace('nan', np.nan)
        st.session_state['scores_rag'] = scores_rag

    # Responses
    if 'responses' not in st.session_state:
        responses = conn.query('SELECT * FROM aggregate_responses;')
        st.session_state['responses'] = responses

    # Overall counts
    if 'counts' not in st.session_state:
        counts = conn.query('SELECT * FROM overall_counts;')
        counts['count'] = pd.to_numeric(counts['count'], errors='ignore')
        st.session_state['counts'] = counts

    # Demographic
    if 'demographic' not in st.session_state:
        demographic = conn.query('SElECT * FROM aggregate_demographic;')
        st.session_state['demographic'] = demographic

    # Run tests to check whether these match the csv files
    if tests:
        assert_frame_equal(
            st.session_state.scores,
            pd.read_csv('data/survey_data/aggregate_scores.csv'))
        assert_frame_equal(
            st.session_state.scores_rag,
            pd.read_csv('data/survey_data/aggregate_scores_rag.csv'))
        assert_frame_equal(
            st.session_state.responses,
            pd.read_csv('data/survey_data/aggregate_responses.csv'))
        assert_frame_equal(
            st.session_state.counts,
            pd.read_csv('data/survey_data/overall_counts.csv'))
        assert_frame_equal(
            st.session_state.demographic,
            pd.read_csv('data/survey_data/aggregate_demographic.csv'))