'''
Helper function for importing the data from TiDB Cloud
'''
import numpy as np
import pandas as pd
import streamlit as st
from pandas.testing import assert_frame_equal
from tempfile import NamedTemporaryFile
import pymysql


def get_df(query, conn):
    '''
    Get data from the connected SQL database

    Parameters:
    -----------
    query : string
        SQL query
    conn : connection object
        Connection to the SQL database

    Returns:
    --------
    df : pandas DataFrame
        Dataframe produced from the query
    '''
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(cursor.fetchall(), columns=columns)
    return df


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
    # First, check if everything is in the session state - if so, don't need to
    # connect, but if missing stuff, will want to connect
    items = ['scores', 'scores_rag', 'responses', 'counts', 'demographic']

    if not all([x in st.session_state for x in items]):

        # Create temporary PEM file for setting up the connection
        with NamedTemporaryFile(suffix='.pem') as temp:

            # Write the temporary file
            temp.write(st.secrets.tidb.root_cert.encode('utf-8'))

            # Temporary file have pointer to current position in file - as we
            # have just written, the pointer is at the end of the last write,
            # so if you don't seek, you would read from the end of the file and
            # find nothing
            temp.seek(0)

            # Set up connection manually, providing the temporary PEM file
            # (as cannot use st.connection() without providing tempfile name
            # in secrets)
            conn = pymysql.connect(
                host=st.secrets.tidb.host,
                user=st.secrets.tidb.username,
                password=st.secrets.tidb.password,
                database=st.secrets.tidb.database,
                port=st.secrets.tidb.port,
                ssl_verify_cert=False,
                ssl_verify_identity=False,
                ssl_ca=temp.name
            )

            # Scores
            if 'scores' not in st.session_state:
                scores = get_df('SELECT * FROM aggregate_scores;', conn)
                st.session_state['scores'] = scores

            # Scores RAG
            if 'scores_rag' not in st.session_state:
                scores_rag = get_df(
                    'SELECT * FROM aggregate_scores_rag;', conn)
                # Convert columns to numeric
                to_fix = ['mean', 'count', 'total_pupils', 'group_n',
                          'group_wt_mean', 'group_wt_std', 'lower', 'upper']
                for col in to_fix:
                    scores_rag[col] = pd.to_numeric(scores_rag[col],
                                                    errors='ignore')
                # Convert string 'nan' to actual np.nan
                scores_rag['rag'] = scores_rag['rag'].replace('nan', np.nan)
                st.session_state['scores_rag'] = scores_rag

            # Responses
            if 'responses' not in st.session_state:
                responses = get_df('SELECT * FROM aggregate_responses;', conn)
                st.session_state['responses'] = responses

            # Overall counts
            if 'counts' not in st.session_state:
                counts = get_df('SELECT * FROM overall_counts;', conn)
                counts['count'] = pd.to_numeric(counts['count'],
                                                errors='ignore')
                st.session_state['counts'] = counts

            # Demographic
            if 'demographic' not in st.session_state:
                demographic = get_df(
                    'SElECT * FROM aggregate_demographic;', conn)
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
