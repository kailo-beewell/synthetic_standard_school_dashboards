'''
Function to generate a non-interactive PDF version of the dashboard as a
temporary file that can then be downloaded from the dashboard
'''
import os
import base64
from markdown import markdown
from utilities.reshape_data import get_school_size
from utilities.summary_rag import summary_intro, summary_table
from utilities.explore_results import (
    write_page_title,
    create_topic_dict,
    create_explore_topic_page)
from utilities.who_took_part import (
    create_demographic_page_intro,
    demographic_headers,
    demographic_plots)
from utilities.reuse_text import text_how_use, text_caution_comparing


def create_static_report(chosen_school, chosen_group, df_scores, df_prop,
                         counts, dem_prop, pdf_title):
    '''
    Generate a static PDF report for the chosen school and group, with all
    the key information and figures from the dashboard

    Parameters
    ----------
    chosen_school : string
        Name of the chosen school
    chosen_group : string
        Name of the chosen group to view results by - options are
        'For all pupils', 'By year group', 'By gender', 'By FSM' or 'By SEN'
    df_scores : dataframe
        Dataframe with aggregate scores and RAG for each topic
    df_prop : dataframe
        Dataframe with proportion of each response to each survey question
    counts : dataframe
        Dataframe with the counts of pupils at each school
    dem_prop : dataframe
        Dataframe with proportion of each reponse to the demographic questions
    pdf_title : string
        Title for the PDF file
    '''
    ##########
    # Set-up #
    ##########

    # Create empty list to fill with HTML content for PDF report
    content = []

    # Get dictionaries which will use later on and for table of contents
    # Create dictionary of topics
    topic_dict = create_topic_dict(df_scores)
    # Create header dictionary for the demographic section
    dem_header_dict = demographic_headers()

    # Get school size
    school_size = get_school_size(counts, chosen_school)

    ##############
    # Title page #
    ##############

    # Logo - convert to HTML, then add to the content for the report
    data_uri = base64.b64encode(open('images/kailo_beewell_logo_padded.png',
                                     'rb').read()).decode('utf-8')
    img_tag = f'''
<img src='data:image/png;base64,{data_uri}' alt='Kailo #BeeWell logo'
style='width:300px; height:182px;'>'''
    content.append(img_tag)

    # Get group name with only first character modified to lower case
    group_lower_first = chosen_group[0].lower() + chosen_group[1:]

    # Title and introduction
    title_page = f'''
<div class='section_container'>
    <h1 style='text-align:center;'>The #BeeWell Survey</h1>
    <p style='text-align:center; font-weight:bold;'>Thank you for taking
    part in the #BeeWell survey delivered by Kailo.</p>
    <p>The results from pupils at your school can be explored using the
    interactive dashboard at
    https://synthetic-beewell-kailo-standard-school-dashboard.streamlit.app/.
    This report has been downloaded from that dashboard.<br><br>
    There are four reports available - these have results: (a) from all
    pupils, (b) by gender, (c) by free school meal (FSM) eligibility, and
    (d) by year group.<br><br>
    This report contains the results <b>{group_lower_first}</b> for
    <b>{chosen_school}</b>.</p>
</div>
'''
    content.append(title_page)

    # Illustration - convert to HTML, then add to the content for the report
    data_uri = base64.b64encode(open('images/home_image_3_transparent.png',
                                     'rb').read()).decode('utf-8')
    img_tag = f'''
<img src='data:image/png;base64,{data_uri}' alt='Kailo illustration'
style='width:650px; height:192px;'>'''
    illustration = f'''
<div style='width:100%; position:absolute; bottom:0;'>
    {img_tag}
</div>'''
    content.append(illustration)

    ################
    # Introduction #
    ################

    # Heading
    content.append('''<h1 style='page-break-before:always;'>
                   Introduction</h1>''')

    # Using the report (duplicate text with About.py)
    content.append('<h2>How to use this report</h2>')
    content.append(markdown(text_how_use()))

    # Comparison warning (duplicate text with Explore results.py)
    content.append('<h2>Comparing between schools</h2>')
    content.append(markdown(text_caution_comparing()))

    #####################
    # Table of contents #
    #####################

    # Get all of the explore results pages as lines for the table of contents
    explore_results_pages = []
    for key, value in topic_dict.items():
        line = f'''<li><a href='#{value}'>{key}</a></li>'''
        explore_results_pages.append(line)

    # Get the demographic headers as lines for the table of contents
    demographic_pages = []
    for key, value in dem_header_dict.items():
        line = f'''<li><a href='#{key}'>{value}</a></li>'''
        demographic_pages.append(line)

    content.append(f'''
<div>
    <h1 style='page-break-before:always;'>Table of Contents</h1>
    <ul>
        <li><a href='#summary'>Summary</a> - See a simple overview of
            results from pupils at your school, compared with other
            schools</li>
        <br>
        <li><a href='#explore_results'>Explore results</a> - Explore how
            your pupils responded to each survey question, and see further
            information on how the summary page's comparison to other
            schools was generated
            <ul>{''.join(explore_results_pages)}</ul>
        </li>
        <br>
        <li><a href='#who_took_part'>Who took part</a> - See the
            characteristics of the pupils who took part in the survey
            <ul>{''.join(demographic_pages)}</ul>
        </li>
    </ul>
</div>
''')

    ################
    # Summary page #
    ################

    # Summary cover page with guide to RAG ratings
    content.append(summary_intro(school_size, 'pdf'))

    # Summary grid with RAG ratings for each topic
    content = summary_table(
        df_scores, chosen_group, chosen_school, 'pdf', content)

    ###########################
    # Explore results section #
    ###########################

    # Craete cover page with title and introduction
    content.append(write_page_title(output='pdf'))

    # Create pages for all of the topics
    for chosen_variable_lab in topic_dict.keys():
        content = create_explore_topic_page(
            chosen_variable_lab, topic_dict, df_scores, chosen_school,
            chosen_group, df_prop, content)

    #########################
    # Who took part section #
    #########################

    # Create cover page with title and introduction
    content.append(create_demographic_page_intro(school_size, 'pdf'))

    # Create pages with plots for each measure
    content = demographic_plots(
        dem_prop=dem_prop, chosen_school=chosen_school,
        chosen_group='Compared with other schools in Northern Devon',
        output='pdf', content=content)

    ######################
    # Create HTML report #
    ######################

    # Remove the final temporary image file
    if os.path.exists('report/temp_image.png'):
        os.remove('report/temp_image.png')

    # Import the CSS stylesheet
    with open('css/static_report_style.css') as css:
        css_style = css.read()

    html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <title>{pdf_title}</title>
    <style>
        {css_style}
    </style>
</head>
<body>
    {''.join(content)}
</body>
</html>
'''

    return html_content
