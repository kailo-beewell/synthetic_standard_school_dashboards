'''
Functions used for the streamlit page Details.py
'''
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utilities.colours import linear_gradient


def survey_responses(dataset, chosen_group='For all pupils'):
    '''
    Create bar charts for each of the quetsions in the provided dataframe.
    The dataframe should contain questions which all have the same set
    of possible responses.
    Inputs:
    - df, dataframe - e.g. chosen_result
    - chosen_group, string - determines whether it will be 2 bars or 1 per plot
    '''
    font_size=18

    # Create seperate figures for each of the measures
    for measure in dataset['measure_lab'].drop_duplicates():

        # Use containers to help visually seperate plots
        with st.container(border=True):
            
            # Create header for plot (use markdown instead of plotly title as the
            # plotly title overlaps the legend if it spans over 2 lines)
            st.markdown(f'**{measure}**')

            # Filter to the relevant measure
            df = dataset[dataset['measure_lab'] == measure]

            # Create colour map
            if chosen_group=='For all pupils':
                colour_map = {'All': '#FF6E4A'}
            else:
                colour_map = {np.unique(df['group'])[0]: '#ffb49a',
                            np.unique(df['group'])[1]: '#e05a38'}

            # Create figure
            fig = px.bar(
                df, x='cat_lab', y='percentage',
                # Set colours and grouping
                color='group', barmode='group', color_discrete_map=colour_map,
                # Label bars with the percentage to 1 decimal place
                text_auto='.1f',
                # Specify what to show when hover over the bars
                hover_data={
                    'cat_lab': True,
                    'percentage': ':.1f',
                    'count': True,
                    'measure_lab': False,
                    'group': False})

            # Set x axis to type category, else only shows integer categories if you
            # have a mix of numbers and strings
            fig.update_layout(xaxis_type='category')

            # Add percent sign to the numbers labelling the bars
            fig.for_each_trace(lambda t: t.update(texttemplate = t.texttemplate + ' %'))

            # Make changes to figure design...
            fig.update_layout(
                # Set font size of bar labels
                font = dict(size=font_size),
                # Set x axis title, labels, colour and size
                xaxis = dict(
                    title='Question response',
                    tickfont=dict(color='#05291F', size=font_size),
                    titlefont=dict(color='#05291F', size=font_size)),
                # Set y axis title, labels, colour and size
                yaxis = dict(
                    title='Percentage of pupils providing response',
                    titlefont=dict(color='#05291F', size=font_size),
                    tickfont=dict(color='#05291F', size=font_size),
                    ticksuffix='%'
                ),
                # Legend title and labels and remove interactivity
                legend = dict(
                    title='Pupils',
                    font=dict(color='#05291F', size=font_size),
                    itemclick=False, itemdoubleclick=False),
                # Legend title font
                legend_title = dict(
                    font=dict(color='#05291F', size=font_size)))

            # Disable zooming and panning
            fig.layout.xaxis.fixedrange = True
            fig.layout.yaxis.fixedrange = True

            # Create plot on streamlit app, hiding the plotly settings bar
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def details_ordered_bar(school_scores, school_name):
    '''
    Created ordered bar chart with the results from each school, with the
    chosen school highlighted
    Inputs:
    - school_scores, dataframe with mean score at each school (e.g. between_schools)
    - school_name, string, name of school (matching name in 'school_lab' col)
    '''
    # Make a copy of the school_scores df to work on (avoid SettingCopyWarning)
    df = school_scores.copy()

    # Add colour for bar based on school
    df['colour'] = np.where(
        df['school_lab']==school_name, 'Your school', 'Other schools')

    # Create column with mean rounded to 2 d.p.
    df['Mean score'] = round(df['mean'], 2)

    # Plot the results, specifying colours and hover data
    fig = px.bar(
        df, x='school_lab', y='mean', color='colour',
        color_discrete_map={'Your school': '#5D98AB', 'Other schools': '#BFD8E0'},
        category_orders={'colour': ['Your school', 'Other schools']},
        hover_data={'school_lab': False, 'colour': False,
                    'mean': False, 'Mean score': True})

    # Reorder x axis so in ascending order
    fig.update_layout(xaxis={'categoryorder':'total ascending'})

    # Set y axis limits so the first and last bars of the chart a consistent height
    # between different plots - find 15% of range and adj min and max by that
    min = df['mean'].min()
    max = df['mean'].max()
    adj_axis = (max - min)*0.15
    ymin = min - adj_axis
    ymax = max + adj_axis
    fig.update_layout(yaxis_range=[ymin, ymax])

    # Extract lower and upper rag boundaries amd shade the RAG areas
    # (Colours used were matched to those from the summary page)
    lower = df['lower'].to_list()[0]
    upper = df['upper'].to_list()[0]
    fig.add_hrect(y0=ymin, y1=lower, fillcolor='#FFCCCC', layer='below',
                line={'color': '#9A505B'}, line_width=0.5,
                annotation_text='Below average', annotation_position='top left')
    fig.add_hrect(y0=lower, y1=upper, fillcolor='#FFE8BF', layer='below',
                line={'color': '#B3852A'}, line_width=0.5,
                annotation_text='Average', annotation_position='top left')
    fig.add_hrect(y0=upper, y1=ymax, fillcolor='#B6E6B6', layer='below',
                line={'color': '#3A8461'}, line_width=0.5,
                annotation_text='Above average', annotation_position='top left')

    # Set font size and hide x axis tick labels (but seems to be a bug that
    # means the axis label is then above the plot, so had to use a work around
    # of replacing the axis labels with spaces
    font_size = 18
    fig.update_layout(
        font = dict(size=font_size),
        xaxis = dict(title='Northern Devon schools (ordered by mean score)',
                     title_font_size=font_size,
                     tickvals=df['school_lab'],
                     ticktext=[' ']*len(df['school_lab'])),
        yaxis = dict(title='Mean score',
                     title_font_size=font_size,
                     tickfont=dict(size=font_size)),
        legend = dict(font_size=font_size),
        legend_title_text=''
    )

    # Prevent zooming and panning, remove grid, and hide plotly toolbar
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True
    fig.update_yaxes(showgrid=False)

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})