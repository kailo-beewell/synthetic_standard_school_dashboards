import plotly.express as px
import pandas as pd
import numpy as np
from ast import literal_eval
from utilities.bar_charts import survey_responses
#import kaleido
import os
import weasyprint

# Import functions I have defined elsewhere
from utilities.bar_charts import survey_responses
from utilities.bar_charts_text import create_response_description
from utilities.explore_results import create_topic_dict, write_topic_intro, write_response_section_intro, get_chosen_result

chosen_variable_lab = 'Autonomy'
chosen_group = 'For all pupils'
chosen_school = 'School A'

# Import data
df_scores = pd.read_csv('data/survey_data/aggregate_scores_rag.csv')
df_prop = pd.read_csv('data/survey_data/aggregate_responses.csv')

# Create empty list to fill with HTML content for PDF report
content = []

# Create dictionary of topics
topic_dict = create_topic_dict(df_scores)

# Convert from variable_lab to variable
chosen_variable = topic_dict[chosen_variable_lab]

# Topic header and description
content = write_topic_intro(chosen_variable, chosen_variable_lab, df_scores,
                            output='pdf', content=content)

# Section header and description
content = write_response_section_intro(
    chosen_variable_lab, output='pdf', content=content)

# Get dataframe with results for the chosen variable, group and school
chosen_result = get_chosen_result(
    chosen_variable, chosen_group, df_prop, chosen_school)

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

# Create stacked bar chart with seperate charts if required
if chosen_variable in multiple_charts:
    var_dict = multiple_charts[chosen_variable]
    for key, value in var_dict.items():
        # Add description
        if key in response_descrip.keys():
            content.append(f'<p>{response_descrip[key]}</p><br>')
        # Create plot (reversing the categories if required)
        to_plot = chosen_result[chosen_result['measure'].isin(value)]
        if key in reverse:
            to_plot = reverse_categories(to_plot)
        content = survey_responses(
            dataset=to_plot, font_size=14, output='pdf', content=content)

# Otherwise create a single stacked bar chart
else:
    # Add description
    if chosen_variable in response_descrip.keys():
        content.append(f'<p>{response_descrip[chosen_variable]}</p><br>')
    # Create plot (reversing the categories if required)
    if chosen_variable in reverse:
        chosen_result = reverse_categories(chosen_result)
    content = survey_responses(
        dataset=chosen_result, font_size=14, output='pdf', content=content)


# Remove the final temporary image file
if os.path.exists('report/temp_image.png'):
    os.remove('report/temp_image.png')

# Source Sans Pro is the sans-serif font used by Streamlit, but was having issues
# with getting bold typeface, so switched to use default 'sans-serif' which was fine
# #05291F is Kailo's dark green colour.
css_style = '''
body {
    font-family: sans-serif;
    color: #05291F;
}
.img_container {
    border-radius: 25px;
    border: 2px solid #D7D7D7;
    padding-left: 20px;
    padding-right: 20px;
    padding-top: 15px;
    padding-bottom: 10px;
    page-break-inside: avoid;
}
h2 {
    font-size: 40px;
    margin: 0;
}
p {
    font-size: 14px;
}
@page {
    @top-right{
        content: 'Page ' counter(page) ' of ' counter(pages);
        font-family: sans-serif;
        font-size: 10px;
    }
}
'''

html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>#BeeWell Kailo School Report 2024</title>
    <style>
        {css_style}
    </style>
</head>
<body>
    {''.join(content)}
</body>
</html>
'''

# Generate HTML (not used currently to make PDF report, but useful if want to inspect)
with open('report/report.html', 'w') as f:
    f.write(html_content)

# Create PDF using Weasyprint (better)
weasyprint.HTML(string=html_content).write_pdf('report/report.pdf')