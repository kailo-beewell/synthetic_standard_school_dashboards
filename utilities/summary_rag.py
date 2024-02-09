'''
Helper functions for the summary page, and for the production of the 'RAG'
boxes which are also use on the 'Explore Results' page
'''
import pandas as pd


def result_box(rag):
    '''
    Creates a result box with the RAG rating

    Parameters
    ----------
    rag : string
        Result from comparison with other schools - either 'below', 'average',
        'above', or np.nan

    Returns
    -------
    box : string
        HTML string, to be appended to the content for the report
    '''
    # Create the results box
    if rag == 'below':
        box = '''
<div class='result_box' style='background: #FFCCCC; color: #95444B'>
    <p>Below average</p>
</div>'''
    elif rag == 'average':
        box = '''
<div class='result_box' style='background: #FFE8BF; color: #AA7A18'>
    <p>Average</p>
</div>'''
    elif rag == 'above':
        box = '''
<div class='result_box' style='background: #B6E6B6; color: #2B7C47'>
    <p>Above average</p>
</div>'''
    elif pd.isnull(rag):
        box = '''
<div class='result_box' style='background: #DCE4FF; color: #19539A'>
    <p>n < 10</p>
</div>'''

    return box


def rag_intro_column(rag, rag_descrip):
    '''
    Generate a row for the introduction to the summary section, with a RAG
    box and description of that box across 2 columns.

    Parameters
    ----------
    rag : string
        RAG performance - either 'above', 'average', 'below', or np.nan
    rag_descrip : string
        Description of the RAG rating

    Returns
    -------
    html : string
        Section of HTML that creates the RAG introductory columns
    '''
    rag_box = result_box(rag)
    html = f'''
<div class='row'>
    <div class='column' style='margin-top:0.5em;'>
        {rag_box}
    </div>
    <div class='column'>
        {rag_descrip}
    </div>
</div>
'''
    return html
