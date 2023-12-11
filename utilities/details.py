'''
Functions used for the streamlit page Details.py
'''
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utilities.colours import linear_gradient


def details_stacked_bar(dataset, chosen_group='For all pupils'):
    '''
    Creates a series of seperate stacked bar charts using the provided
    dataframe, which should contain results for one/a set of variables with the
    same response options. Each plot represents a different question.
    Inputs:
    - df, dataframe - e.g. chosen_result
    - chosen_group, string - determines whether it will be 2 bars or 1 per plot
    '''
    # Specify font size
    font_size = 18

    # Create seperate figures for each of the measures
    for measure in dataset['measure_lab'].drop_duplicates():

        # Create line to help visually seperate out the plots
        st.divider()

        # Create header for plot (use markdown instead of plotly title as the
        # plotly title overlaps the legend if it spans over 2 lines)
        st.markdown(f'**{measure}**')

        # Filter to the relevant measure
        df = dataset[dataset['measure_lab'] == measure]

        # Get colour spectrum between the provided colours, for all except one category
        # Use 'cat_lab' rather than 'cat' as sometimes cat is 0-indexed or 1-indexed
        start_colour = '#5D98AB'
        end_colour = '#FFD700'
        n_cat = df['cat_lab'].drop_duplicates().size

        # Create colour map and pattern map
        # If there is a "less than 10 responses" category, create n-2 colours
        # and set last two as shades of grey, with <10 responses having hashing
        if df['cat_lab'].eq('Less than 10 responses').any():
            colours = linear_gradient(start_colour, end_colour, n_cat-2)['hex']
            colours += ['#DDDDDD']
            colours += ['#DDDDDD']
            pattern_map = ['']*(n_cat-1) + ['/']
        # Do spectrum for all except final colour, which is Missing so set as grey
        # And no patterns to map to
        else:
            colours = linear_gradient(start_colour, end_colour, n_cat-1)['hex']
            colours += ['#DDDDDD']
            pattern_map = False

        if pattern_map:
            # Create the figure
            fig = px.bar(
                # Specify data to plot
                df, x='percentage', y='group',
                # Set colours
                color='cat_lab', color_discrete_sequence=colours,
                # Set hashing
                pattern_shape='cat_lab', pattern_shape_sequence = pattern_map,
                # Label bars with the percentage to 1 decimal place
                text_auto='.1f',
                # Specify what to show when hover over the bars
                hover_data={
                    'cat_lab': True,
                    'percentage': ':.1f',
                    'count': True,
                    'measure_lab': False,
                    'group': False},
                # Remove the title
                title='')
        else:
            # Create the figure
            fig = px.bar(
                # Specify data to plot
                df, x='percentage', y='group',
                # Set colours
                color='cat_lab', color_discrete_sequence=colours,
                # Label bars with the percentage to 1 decimal place
                text_auto='.1f',
                # Specify what to show when hover over the bars
                hover_data={
                    'cat_lab': True,
                    'percentage': ':.1f',
                    'count': True,
                    'measure_lab': False,
                    'group': False},
                # Remove the title
                title='')

        # Add percent sign to the numbers labelling the bars
        fig.for_each_trace(lambda t: t.update(texttemplate = t.texttemplate + ' %'))

        # Set figure height depending on bar number
        if chosen_group=='For all pupils':
            height=240
        else:
            height=300

        # Make changes to figure design...
        fig.update_layout(
            # Set font size of bar labels
            font = dict(size=font_size),
            # titlefont = dict(size=font_size),
            # Set x axis ticks colour and size and to have percentage sign
            xaxis = dict(
                tickmode='array',
                tickvals=[0, 20, 40, 60, 80, 100],
                ticktext=['0%', '20%', '40%', '60%', '80%', '100%'],
                tickfont=dict(color='#05291F', size=font_size),
                title='Percentage of students who gave response',
                titlefont=dict(color='#05291F', size=font_size)),
            # Set y axis font color and size and remove title
            yaxis = dict(
                title='',
                tickfont=dict(color='#05291F', size=font_size)),
            # Customise legend...
            legend = dict(
                # Set tick font size and remove axis title
                font_size=font_size,
                title='',
                # Make legend horizontal and centered above figure
                orientation='h',
                xanchor='center', yanchor='bottom', x=0.5, y=1,
                # Remove legend click interactivity
                itemclick=False, itemdoubleclick=False),
            # Set figure height
            height=height)

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