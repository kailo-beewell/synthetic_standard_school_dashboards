'''
Large sections of text that are re-used between the dashboard and PDF report,
but don't fit into other .py files (for example, if used on different pages -
so on About page for dashboard, and then in Introduction for PDF report)
'''


def text_how_use():
    '''
    Generate a few paragraphs on how to use this report

    Returns
    -------
    text : string
        Markdown-formatted string
    '''
    text = '''
These data can provide a useful starting point for discussions about the needs
of your school population and priority areas for development and improvement.
It can also be useful in considering areas of strengths and/or helping pupils
reflect on their positive qualities.

Data in your #BeeWell report may be useful in indicating progress against
targets in your School Improvement Plan or help to identify future target
areas. It may help to identify areas of priority for staff training or be used
as context when considering academic data for participating year groups. It can
also be used as independent evidence in the context of an Ofsted inspection.

Finally, young people consulted during the set-up of #BeeWell in Greater
Manchester felt strongly that pupils should be included in discussions around
feedback, particularly to plan activities and approaches to raise awareness of
strengths or difficulties the #BeeWell survey may highlight. They suggested
involving a range of students (not just those involved in school councils) in
planning how to raise awareness about wellbeing and to support the needs of
young people.'''
    return text


def text_caution_comparing():
    '''
    Generate a few paragraphs to caution around comparisons

    Returns
    -------
    text : string
        Markdown-formatted string
    '''
    text = '''
Always be mindful when making comparisons between different schools. There are
a number of factors that could explain differences in scores (whether you are
above average, average, or below average). These include:

* Random chance ('one-off' findings).
* Differences in the socio-economic characteristics of pupils and the areas
where they live (e.g. income, education, ethnicity, access to services and
amenities).
* The number of pupils taking part - schools that are much smaller are more
likely to have more "extreme" results (i.e. above or below average), whilst
schools with a larger number of pupils who took part are more likely to
see average results

It's also worth noting that the score will only include results from pupils who
completed each of the questions used to calculate that topic - so does not
include any reflection of results from pupils who did not complete some or all
of the questions for that topic.
'''
    return text

# Draft phrasing for benchmarking (not currently included in dashboards):
# When comparing to the Greater Manchester data, be aware that (i) there
# are likely to be greater differences in population characteristics
# between Northern Devon and Greater Manchester than between different
# areas in Northern Devon, and (ii) the Greater Manchester data were
# collected in Autumn Term 2021 while the Havering data was collected in
# Summer Term 2023.
