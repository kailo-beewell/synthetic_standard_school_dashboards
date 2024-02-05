import plotly.express as px
import pandas as pd
import numpy as np
from ast import literal_eval
from utilities.bar_charts import survey_responses
import kaleido
import base64
import plotly
import os
import markdown
import weasyprint
from io import BytesIO

from utilities.bar_charts_text import create_response_description

chosen_variable_lab = 'Autonomy'
chosen_group = 'For all pupils'
school = 'School A'

# Import data
df_scores = pd.read_csv('data/survey_data/aggregate_scores_rag.csv')
df_prop = pd.read_csv('data/survey_data/aggregate_responses.csv')

content = []

# Create dictionary of topics
topic_df = df_scores[['variable', 'variable_lab']].drop_duplicates()
topic_df = topic_df[~topic_df['variable'].isin([
        'staff_talk_score', 'home_talk_score', 'peer_talk_score'])]
topic_df['variable'] = topic_df['variable'].str.replace('_score', '')
topic_dict = pd.Series(topic_df.variable.values, index=topic_df.variable_lab).to_dict()

# Convert from variable_lab to variable
chosen_variable = topic_dict[chosen_variable_lab]

# Create dictionary of descriptions, where index is the variable
description = df_scores[['variable', 'description']].drop_duplicates().set_index('variable').to_dict()['description']

# Write text
content.append(f'''<h2 style='font-size:55px;text-align:center;'>{chosen_variable_lab}</h2>''')
content.append(f'''<p style='text-align:center;'><b>These questions are about {description[f'{chosen_variable}_score'].lower()}</b></p>''')
content.append('<h3>Responses from pupils at your school</h3>')
content.append(f'''\
<p>In this section, you can see how pupils at you school responded to survey \
questions that relate to the topic of '{chosen_variable_lab.lower()}'.</p>''')

# Set default values
year_group = ['All']
gender = ['All']
fsm = ['All']
sen = ['All']
group_lab = 'year_group_lab' # set as default group but not used, prevents error

# Depending on chosen breakdown, alter one of the above variables
if chosen_group == 'By year group':
    year_group = ['Year 8', 'Year 10']
    group_lab = 'year_group_lab'
elif chosen_group == 'By gender':
    gender = ['Girl', 'Boy']
            #'I describe myself in another way', 'Non-binary',
            #'Prefer not to say']
    group_lab = 'gender_lab'
elif chosen_group == 'By FSM':
    fsm = ['FSM', 'Non-FSM']
    group_lab = 'fsm_lab'
elif chosen_group == 'By SEN':
    sen = ['SEN', 'Non-SEN']
    group_lab = 'sen_lab'

# Filter to chosen variable and school
chosen = df_prop[
    (df_prop['group'] == chosen_variable) &
    (df_prop['school_lab'] == school) &
    (df_prop['year_group_lab'].isin(year_group)) &
    (df_prop['gender_lab'].isin(gender)) &
    (df_prop['fsm_lab'].isin(fsm)) &
    (df_prop['sen_lab'].isin(sen))]

# Extract the lists with results stored in the dataframe
# e.g. ['Yes', 'No'], [20, 80], [2, 8] in the original data will become
# seperate columns with [Yes, 20, 2] and [No, 80, 8]
df_list = []
for index, row in chosen.iterrows():
    # Extract results as long as it isn't NaN (e.g. NaN when n<10)
    if ~np.isnan(row.n_responses):
        df = pd.DataFrame(zip(literal_eval(row['cat'].replace('nan', 'None')),
                            literal_eval(row['cat_lab']),
                            literal_eval(row['percentage']),
                            literal_eval(row['count'])),
                        columns=['cat', 'cat_lab', 'percentage', 'count'])
        # Replace NaN with max number so stays at end of sequence
        df['cat'] = df['cat'].fillna(df['cat'].max()+1)
        # Add measure (don't need to extract as string rather than list in df)
        df['measure'] = row['measure']
        df['measure_lab'] = row['measure_lab']
        df['group'] = row[group_lab]
        df_list.append(df)
    # As we still want a bar when n<10, we create a record still but label as such
    else:
        df = row.to_frame().T[['measure', 'measure_lab']]
        df['group'] = row[group_lab]
        df['cat'] = 0
        df['cat_lab'] = 'Less than 10 responses'
        df['count'] = np.nan
        df['percentage'] = 100
        df_list.append(df)

chosen_result = pd.concat(df_list)

# For categories with multiple charts, list the variables for each chart
multiple_charts = {
    'optimism': {'optimism_future': ['optimism_future'],
                'optimism_other': ['optimism_best', 'optimism_good', 'optimism_work']},
    'appearance': {'appearance_happy': ['appearance_happy'],
                'appearance_feel': ['appearance_feel']},
    'physical': {'physical_days': ['physical_days'],
                'physical_hours': ['physical_hours']},
    'places': {'places_freq': ['places_freq'],
            'places_barriers': ['places_barriers___1', 'places_barriers___2',
                                'places_barriers___3', 'places_barriers___4',
                                'places_barriers___5', 'places_barriers___6',
                                'places_barriers___7', 'places_barriers___8',
                                'places_barriers___9']},
    'talk': {'talk_yesno': ['staff_talk', 'home_talk', 'peer_talk'],
            'talk_listen': ['staff_talk_listen', 'home_talk_listen', 'peer_talk_listen'],
            'talk_helpful': ['staff_talk_helpful', 'home_talk_helpful', 'peer_talk_helpful'],
            'talk_if': ['staff_talk_if', 'home_talk_if', 'peer_talk_if']},
    'local_env': {'local_safe': ['local_safe'],
                'local_other': ['local_support', 'local_trust',
                                'local_neighbours', 'local_places']},
    'future': {'future_options': ['future_options'],
            'future_interest': ['future_interest'],
            'future_support': ['future_support']}
}
# Import descriptions for stacked bar charts
response_descrip = create_response_description()

# Categories to reverse - exceptions were media and bully, as the order when
# negative to positive felt counter-intuitive
reverse = ['esteem', 'negative', 'support', 'free_like', 'local_safe',
        'local_other', 'belong_local', 'bully']

def reverse_categories(df):
    '''
    Resorts dataframe so categories are in reverse order, but non-respones is
    still at the end (despite being max value).
    Inputs:
    df - dataframe to sort
    '''
    # Resort everything except for the pupils who did not respond (which is
    # always the final category)
    new_df = df[df['cat'] != df['cat'].max()].sort_values(by=['cat'], ascending=False)
    # Append those non-response counts back to the end
    new_df = pd.concat([new_df, df[df['cat'] == df['cat'].max()]])
    # Return the resorted dataframe
    return(new_df)

def survey_responses(dataset, content, font_size=16):
    '''
    Create bar charts for each of the questions in the provided dataframe.
    The dataframe should contain questions which all have the same set
    of possible responses.

    Parameters
    ----------
    df : dataframe
        Dataframe to create plot from (e.g. chosen_result)
    font_size : integer
        Font size of x axis labels, y axis labels and legend text, default=16
    '''
    # Create seperate figures for each of the measures
    for measure in dataset['measure_lab'].drop_duplicates():
            
        # Create header for plot (use markdown instead of plotly title as the
        # plotly title overlaps the legend if it spans over 2 lines)
        content.append(f'<p><strong>{measure}</strong></p>')

        # Filter to the relevant measure
        df = dataset[dataset['measure_lab'] == measure]

        # Check if there are any groups where n<10
        mask = df['cat_lab'] == 'Less than 10 responses'
        under_10 = df[mask]
        # If one of the groups are n<10, remove from the dataframe and print
        # explanation
        if len(under_10.index) == 1:
            # Remove group from dataframe
            df = df[~mask]
            # Print explanation
            dropped = np.unique(under_10['group'])[0]
            kept = np.unique(df['group'])[0]
            content.append(f'''<p>There were less than 10 responses from {dropped} pupils so results are just shown for {kept} pupils.</p>''')

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
                title='Response',
                tickfont=dict(color='#05291F', size=font_size),
                titlefont=dict(color='#05291F', size=font_size)),
            # Set y axis title, labels, colour and size
            yaxis = dict(
                title='Percentage of pupils<br>providing response',
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

        # Set to image dimensions as shown in streamlit
        # Set automargin=True so that it adjusts figure so that the labels aren't cut off
        fig.update_layout(
            #height=450,
            #width=657,
            xaxis=dict(automargin=True),
            yaxis=dict(automargin=True)
        )

        # Write image to PNG then link HTML to that file
        #fig.write_image(f'report/images/report_{measure}.png')
        #img_tag = f'''<img src='{os.getcwd()}/report/report_{measure}.png' alt='{measure}' />'''

        # Write image to PNG then insert directly HTML
        fig.write_image(f'report/temp_image.png')
        data_uri = base64.b64encode(
            open(f'report/temp_image.png', 'rb').read()).decode('utf-8')
        img_tag = f'''<img src='data:image/png;base64,{data_uri}' alt='{measure}'>'''
        content.append(img_tag)

        # Write image to HTML
        #fig.write_html(f'report/report_{measure}.html')

    return content

# Create stacked bar chart with seperate charts if required
if chosen_variable in multiple_charts:
    var_dict = multiple_charts[chosen_variable]
    for key, value in var_dict.items():
        # Add description
        if key in response_descrip.keys():
            content.append(f'<p>{response_descrip[key]}</p>')
        # Create plot (reversing the categories if required)
        to_plot = chosen_result[chosen_result['measure'].isin(value)]
        if key in reverse:
            to_plot = reverse_categories(to_plot)
        content = survey_responses(to_plot, content)

# Otherwise create a single stacked bar chart
else:
    # Add description
    if chosen_variable in response_descrip.keys():
        content.append(f'<p>{response_descrip[chosen_variable]}</p>')
    # Create plot (reversing the categories if required)
    if chosen_variable in reverse:
        chosen_result = reverse_categories(chosen_result)
    content = survey_responses(chosen_result, content)


# Remove the final temporary image file
if os.path.exists('report/temp_image.png'):
    os.remove('report/temp_image.png')

# Source Sans Pro is the sans-serif font used by Streamlit
# #05291F is Kailo's dark green colour.
css_style = '''
body {
    font-family: 'Source Sans Pro', sans-serif;
    color: #05291F;
}
'''

html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>Test report</title>
    <link href='https://fonts.googleapis.com/css?family=Source+Sans+Pro' rel='stylesheet' type='text/css'>
    <style>
        {css_style}
    </style>
</head>
<body>
    {''.join(content)}
</body>
</html>
'''

weasyprint.HTML(string=html_content).write_pdf('report/report.pdf')