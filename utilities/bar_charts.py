'''
Functions used to produce the two types of bar chart
'''
import numpy as np
import plotly.express as px
import streamlit as st
from contextlib import nullcontext
from utilities.convert_image import convert_fig_to_html
from markdown import markdown


def survey_responses(dataset, font_size=16, output='streamlit', content=None):
    '''
    Create bar charts for each of the quetsions in the provided dataframe.
    The dataframe should contain questions which all have the same set
    of possible responses.

    Parameters
    ----------
    df : dataframe
        Dataframe to create plot from (e.g. chosen_result)
    font_size : integer
        Font size of x axis labels, y axis labels and legend text, default=16
    output : string
        Use of function - either for streamlit page or PDF report
        Must be either 'streamlit' or 'pdf, default is 'streamlit.
    content : list
        Optional input used when output=='pdf', contains HTML for report.

    Returns
    -------
    content : list
        Optional return, used when output=='pdf', contains HTML for report.
    '''
    # Create seperate figures for each of the measures
    for measure in dataset['measure_lab'].drop_duplicates():

        # Streamlit: Create containers to visually seperate plots
        with (st.container(border=True) if output == 'streamlit'
              else nullcontext()):

            # PDF: Create empty list to store content for PDF
            if output == 'pdf':
                temp_content = []

            # Streamlit and PDF: Create header for plot
            # Don't use in-built plotly title as that overlaps the legend if it
            # spans over 2 lines
            if output == 'streamlit':
                st.markdown(f'**{measure}**')
            elif output == 'pdf':
                temp_content.append(
                    f'''<p style='margin:0;'><strong>{measure}</strong></p>''')

            # Filter to the relevant measure
            df = dataset[dataset['measure_lab'] == measure]

            # Check if there are any groups where n<10 overall - if one of the
            # groups are, remove it from dataframe and print explanation
            mask = df['cat_lab'] == 'Less than 10 responses'
            under_10 = df[mask]
            if len(under_10.index) == 1:
                # Remove group from dataframe
                df = df[~mask]
                # Create explanation
                dropped = np.unique(under_10['group'])[0]
                kept = np.unique(df['group'])[0]
                explanation = f'''
There were less than 10 responses from {dropped} pupils so results are just
shown for {kept} pupils.'''
            elif len(under_10.index) == 2:
                unique_groups = np.unique(df['group'])
                explanation = f'''
There were less than 10 responses from {unique_groups[0]} pupils and from
{unique_groups[1]} pupils, so no results can be shown.'''

            # Print explanation on page for the removal of n<10 overall
            if len(under_10.index) > 0:
                if output == 'streamlit':
                    st.markdown(explanation)
                elif output == 'pdf':
                    temp_content.append(f'<p>{explanation}</p>')

            # Create plot if there was at least one group without NaN
            if len(under_10.index) < 2:

                # First, check for any individual categories censored due to
                # n<10 (this is relevant to demographic page, the explore
                # results page won't have any)
                # If there are any rows with NaN...
                null_mask = df['count'].isnull()
                if sum(null_mask) > 0:
                    # Filter to NaN rows amd get the categories as a string
                    dropped = df.loc[null_mask, ['cat_lab', 'group']]
                    for school in dropped['group'].drop_duplicates():
                        dropped_string = ', '.join(dropped.loc[
                            dropped['group'] == school, 'cat_lab'].values)
                        # Print explanation of this censoring
                        explanation = f'''
Due to small sample sizes, response rates are hidden for:

* {school}: {dropped_string}'''
                        if output == 'streamlit':
                            st.markdown(explanation)
                        elif output == 'pdf':
                            temp_content.append(markdown(explanation))

                # Create colour map
                unique_groups = np.unique(df['group'])
                if (len(unique_groups) == 1):
                    colour_map = {unique_groups[0]: '#FF6E4A'}
                else:
                    colour_map = {unique_groups[0]: '#ffb49a',
                                  unique_groups[1]: '#e05a38'}

                # Create figure
                fig = px.bar(
                    df, x='cat_lab', y='percentage',
                    # Set colours and grouping
                    color='group', barmode='group',
                    color_discrete_map=colour_map,
                    # Label bars with the percentage to 1 decimal place
                    text_auto='.1f',
                    # Specify what to show when hover over the bars
                    hover_data={
                        'cat_lab': True,
                        'percentage': ':.1f',
                        'count': True,
                        'measure_lab': False,
                        'group': False})

                # Set x axis to type category, else only shows integer
                # categories if you have a mix of numbers and strings
                fig.update_layout(xaxis_type='category')

                # Add percent sign to the numbers labelling the bars
                fig.for_each_trace(lambda t: t.update(
                    texttemplate=t.texttemplate + ' %'))

                # Choose survey or council label for y axis, based on tick for
                # x axis ('no response' is survey, 'no data' is council)
                if 'No response' in df['cat_lab'].values:
                    yaxis_title = 'Percentage of pupils<br>providing response'
                else:
                    yaxis_title = 'Percentage of pupils'

                # Make changes to figure design...
                fig.update_layout(
                    # Set font size of bar labels
                    font=dict(size=font_size),
                    # Set x axis title, labels, colour and size
                    xaxis=dict(
                        title='Response',
                        tickfont=dict(color='#05291F', size=font_size),
                        titlefont=dict(color='#05291F', size=font_size)),
                    # Set y axis title, labels, colour and size
                    yaxis=dict(
                        title=yaxis_title,
                        titlefont=dict(color='#05291F', size=font_size),
                        tickfont=dict(color='#05291F', size=font_size),
                        ticksuffix='%'
                    ),
                    # Legend title and labels and remove interactivity
                    legend=dict(
                        title='Pupils',
                        font=dict(color='#05291F', size=font_size),
                        itemclick=False, itemdoubleclick=False),
                    # Legend title font
                    legend_title=dict(
                        font=dict(color='#05291F', size=font_size)))

                # Disable zooming and panning
                fig.layout.xaxis.fixedrange = True
                fig.layout.yaxis.fixedrange = True

                # Streamlit: Create plot on streamlit app, hiding the plotly
                # settings bar
                if output == 'streamlit':
                    st.plotly_chart(fig, use_container_width=True,
                                    config={'displayModeBar': False})

                # PDF: Write image to a temporary PNG file, convert that
                # to HTML, and add the image HTML to temp_content
                elif output == 'pdf':

                    # Make and add HTML image tag to temp_content
                    temp_content.append(convert_fig_to_html(
                        fig=fig, alt_text=measure))

                    # Insert temp_content into a div class and add to content
                    content.append(f'''
    <div class='responses_container'>
        {''.join(temp_content)}
    </div>''')

    # At the end of the loop, if PDF report, return content
    if output == 'pdf':
        return content


def details_ordered_bar(school_scores, school_name, font_size=16,
                        output='streamlit', content=None):
    '''
    Created ordered bar chart with the results from each school, with the
    chosen school highlighted

    Parameters
    ----------
    school_scores : dataframe
        Dataframe with mean score at each school (e.g. between_schools)
    school_name : string
        Name of school (matching name in 'school_lab' col)
    font_size : integer
        Font size of x axis labels, y axis labels and legend text, default=16
    output : string
        Use of function - either for streamlit page or PDF report
        Must be either 'streamlit' or 'pdf, default is 'streamlit.
    content : list
        Optional input used when output=='pdf', contains HTML for report.

    Returns
    -------
    content : list
        Optional return, used when output=='pdf', contains HTML for report.
    '''
    # Make a copy of the school_scores df to work on (avoid SettingCopyWarning)
    df = school_scores.copy()

    # Add colour for bar based on school
    df['colour'] = np.where(
        df['school_lab'] == school_name, 'Your school', 'Other schools')

    # Create column with mean rounded to 2 d.p.
    df['Mean score'] = round(df['mean'], 2)

    # Plot the results, specifying colours and hover data
    fig = px.bar(
        df, x='school_lab', y='mean', color='colour',
        color_discrete_map={'Your school': '#5D98AB',
                            'Other schools': '#BFD8E0'},
        category_orders={'colour': ['Your school', 'Other schools']},
        hover_data={'school_lab': False, 'colour': False,
                    'mean': False, 'Mean score': True})

    # Reorder x axis so in ascending order
    fig.update_layout(xaxis={'categoryorder': 'total ascending'})

    # Set y axis limits so the first and last bars of the chart a consistent
    # height between different plots - find 15% of range and adjust the min
    # and max by that
    min = df['mean'].min()
    max = df['mean'].max()
    adj_axis = (max - min)*0.15
    ymin = np.max([0, (min - adj_axis)])
    ymax = max + adj_axis
    fig.update_layout(yaxis_range=[ymin, ymax])

    # Extract lower and upper rag boundaries amd shade the RAG areas
    # (Colours used were matched to those from the summary page)
    lower = df['lower'].to_list()[0]
    upper = df['upper'].to_list()[0]
    fig.add_hrect(
        y0=ymin, y1=lower, fillcolor='#FFCCCC', layer='below',
        line={'color': '#9A505B'}, line_width=0.5,
        annotation_text='Below average', annotation_position='top left')
    fig.add_hrect(
        y0=lower, y1=upper, fillcolor='#FFE8BF', layer='below',
        line={'color': '#B3852A'}, line_width=0.5,
        annotation_text='Average', annotation_position='top left')
    fig.add_hrect(
        y0=upper, y1=ymax, fillcolor='#B6E6B6', layer='below',
        line={'color': '#3A8461'}, line_width=0.5,
        annotation_text='Above average', annotation_position='top left')

    # Set font size and hide x axis tick labels (but seems to be a bug that
    # means the axis label is then above the plot, so had to use a work around
    # of replacing the axis labels with spaces
    fig.update_layout(
        font=dict(size=font_size),
        xaxis=dict(title='Northern Devon schools<br>(ordered by mean score)',
                   tickfont=dict(color='#05291F', size=font_size),
                   titlefont=dict(color='#05291F', size=font_size),
                   tickvals=df['school_lab'],
                   ticktext=[' ']*len(df['school_lab'])),
        yaxis=dict(title='Mean score',
                   tickfont=dict(color='#05291F', size=font_size),
                   titlefont=dict(color='#05291F', size=font_size)),
        legend=dict(title='School',
                    font=dict(color='#05291F', size=font_size),
                    itemclick=False, itemdoubleclick=False),
        legend_title=dict(font=dict(color='#05291F', size=font_size))
    )

    # Prevent zooming and panning, remove grid, and hide plotly toolbar
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True
    fig.update_yaxes(showgrid=False)

    if output == 'streamlit':
        st.plotly_chart(fig, use_container_width=True,
                        config={'displayModeBar': False})
    elif output == 'pdf':
        # Create temporary list to hold image HTML
        temp_content = []

        # Get the HTML image tag for the figure and add to temp_content
        temp_content.append(convert_fig_to_html(
            fig=fig, alt_text='Comparison with other schools'))

        # Insert temp_content into a div class and add to content
        content.append(f'''
<div class='comparison_container'>
    {''.join(temp_content)}
</div>''')

        # Return the updated content HTML
        return content
