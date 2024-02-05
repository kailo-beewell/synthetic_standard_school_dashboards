# Import required packages
import pandas as pd
#import kaleido
import os
import weasyprint

# Import functions I have defined elsewhere
from utilities.explore_results import (
    write_page_title,
    create_topic_dict,
    write_topic_intro,
    write_response_section_intro,
    get_chosen_result,
    create_bar_charts
)

################################################################################
# Set-up and report section title page

# Create empty list to fill with HTML content for PDF report
content = []

content = write_page_title(output='pdf', content=content)

################################################################################
# Continued set-up and header

chosen_variable_lab = 'Autonomy'
chosen_group = 'For all pupils'
chosen_school = 'School A'

# Import data
df_scores = pd.read_csv('data/survey_data/aggregate_scores_rag.csv')
df_prop = pd.read_csv('data/survey_data/aggregate_responses.csv')

# Create dictionary of topics
topic_dict = create_topic_dict(df_scores)

# Convert from variable_lab to variable
chosen_variable = topic_dict[chosen_variable_lab]

# Topic header and description
content = write_topic_intro(chosen_variable, chosen_variable_lab, df_scores,
                            output='pdf', content=content)

################################################################################
# Responses to each question...

# Section header and description
content = write_response_section_intro(
    chosen_variable_lab, output='pdf', content=content)

# Get dataframe with results for the chosen variable, group and school
chosen_result = get_chosen_result(
    chosen_variable, chosen_group, df_prop, chosen_school)

# Produce bar charts with accompanying chart section descriptions, and titles
content = create_bar_charts(
    chosen_variable, chosen_result, output='pdf', content=content)

################################################################################
# Create HTML report...

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
.page {
    page-break-after: always;
}
.section_container {
    position: absolute;
    top: 30%;
    justify-content: center;
    align-items: center;
    text-align: center;
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