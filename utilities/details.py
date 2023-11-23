'''
Functions used for the streamlit page Details.py
'''
import plotly.express as px
import streamlit as st
import textwrap as tr
from utilities.colours import linear_gradient

def wrap_text(string, width):
    '''
    Wrap the provided string to the specified width, producing a single string
    with new lines indicated by '<br>'. If string length is less than the
    specified width, add blank space to the start of the string (so it will
    still occupy the same amount of space on the chart)
    Inputs:
    - string: str, to wrap
    - width: int, maximum length per line
    '''
    # Wrap string with new lines indicated by <br>
    wrap = '<br>'.join(tr.wrap(string, width=width))
    # If the whole string is less than the chosen width, at blank spaces to
    # the start to it reaches that width
    if len(wrap) < width:
        blank = width - len(wrap)
        wrap=(' '*blank) + wrap
    # If string is greater than width (will therefore have breaks), at blank
    # space to the beginning of the first line so that it reaches the 
    # maximum width
    elif len(wrap) > width:
        first_line = wrap.split('<br>')[0]
        if len(first_line) < width:
            blank = width - len(first_line)
            wrap=(' '*blank) + wrap
    return(wrap)


def details_stacked_bar(df):
    '''
    Create stacked bar chart for detail page using the provided dataframe,
    which should contain results for one/a set of variables with the same
    response options
    Inputs:
    - df, dataframe - e.g. chosen_result
    '''
    # Get colour spectrum between the provided colours, for all except one category
    # Use 'cat_lab' rather than 'cat' as sometimes cat is 0-indexed or 1-indexed
    start_colour = '#2A52BE'
    end_colour = '#D4DCF2'
    n_cat = df['cat_lab'].drop_duplicates().size
    colours = linear_gradient(start_colour, end_colour, n_cat-1)['hex']
    # Add final colour of grey for the last category, which will be "missing"
    colours += ['#DDDDDD']

    # Wrap the labels for each measure
    df['measure_lab_wrap'] = df['measure_lab'].apply(
        lambda x: wrap_text(x, 50))

    # Create plot
    fig = px.bar(
        df, x='percentage', y='measure_lab_wrap', color='cat_lab',
        text_auto=True, orientation='h', color_discrete_sequence=colours,
        hover_data={'cat_lab': True, 'percentage': True,
                    'measure_lab_wrap': False, 'count': True},)

    # Add percent sign to the numbers labelling the bars
    fig.for_each_trace(lambda t: t.update(texttemplate = t.texttemplate + ' %'))

    # Set x axis ticks to include % sign, and remove the axis titles
    fig.update_layout(xaxis = dict(
        tickmode='array',
        tickvals=[0, 20, 40, 60, 80, 100],
        ticktext=['0%', '20%', '40%', '60%', '80%', '100%'],
        title=''))
    fig.update_layout(yaxis_title=None)

    # Set font size
    font_size = 18
    fig.update_layout(
        font = dict(size=font_size),
        xaxis = dict(tickfont=dict(size=font_size)),
        yaxis = dict(tickfont=dict(size=font_size)),
        legend = dict(font_size=font_size)
    )

    # Find number of variables being plot, then set height of figure based on that
    # so the bars appear to be fairly consistent height between different charts
    n_var = df['measure_lab'].drop_duplicates().size
    height = {
        1: 200,
        2: 270,
        3: 350,
        4: 400,
        5: 500,
        6: 600,
        7: 600,
        8: 700,
        9: 800,
        10: 750
    }
    fig.update_layout(autosize=True, height=height[n_var])

    # Make legend horizontal and center on 0.5, and lower on y so not overlapping
    # with the title (which have to adjust depending on nvar, with values
    # identified manually through trial and error)
    y_pos = {
        1: -2,
        2: -0.3,
        3: -0.2,
        4: -0.17,
        5: -0.15,
        6: -0.13,
        7: -0.1,
        8: -0.1,
        9: -0.1,
        10: -0.1
    }
    fig.update_layout(legend=dict(
        orientation='h',
        x=0.5,
        xanchor='center',
        y=y_pos[n_var],
        title=''))

    # Disable zooming and panning
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True

    # Create plot on streamlit app
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})