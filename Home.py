import streamlit as st
from utilities.page_setup import page_setup, blank_lines
from utilities.authentication import check_password

# Set page configuration
page_setup()

if check_password():

    # Add name of school (to help with monitoring)
    st.markdown(st.session_state.school)

    # Title and introduction
    st.title('The #BeeWell Survey')
    st.markdown(f'''
    <p style='text-align: center; font-weight: bold'>
    Thank you for taking part in the #BeeWell survey delivered by Kailo.<br>
    You can use this dashboard to explore results from pupils at your school.</p>
    ''', unsafe_allow_html=True)

    # Image
    st.image('images/home_image_3_transparent.png', use_column_width=True)

    # Pages of the dashboard
    st.subheader('What each page of the dashboard can tell you')
    st.markdown('''
    There are four pages to see on this dashboard, which you can navigate to using
    the sidebar on the left. These are:
    * **About** - Read information on the #BeeWell survey, Kailo, and this dashboard
    * **Summary** - See a simple overview of results from pupils at your school, compared
    with other schools
    * **Explore results** - Explore how your pupils responded to each survey
    question, and see further information on how the summary page's comparison to
    other schools was generated
    * **Who took part** - See the characteristics of the pupils who took part in the
    survey
    ''')

    # This allows you to download a PDF - currently downloading survey - will need
    # to change to a full version of the report - however, this PDF is stored in
    # GitHub, so will need to look if it can pull the PDF from a database else
    # you'd need to generate on click. Also, if we'd need five reports for each of
    # the filters.
    st.subheader('Download PDF report')
    st.markdown('''
    You can use the interactive dashboard to explore results for your school. We
    also provide the option of downloading a PDF version of your resuts below.
    This section is incomplete - currently downloads survey booklet instead.
    ''')
    pdf_report = open('pdfs/survey_v21b.pdf', 'rb')
    st.download_button(
        label='Download school report (all pupils)', data=pdf_report,
        file_name='test_streamlit_download.pdf', mime='application/pdf')
    st.download_button(
        label='Download school report (by gender)', data=pdf_report,
        file_name='test_streamlit_download.pdf', mime='application/pdf')
    st.download_button(
        label='Download school report (by year group)', data=pdf_report,
        file_name='test_streamlit_download.pdf', mime='application/pdf')
    st.download_button(
        label='Download school report (by FSM)', data=pdf_report,
        file_name='test_streamlit_download.pdf', mime='application/pdf')
    st.download_button(
        label='Download school report (by SEN)', data=pdf_report,
        file_name='test_streamlit_download.pdf', mime='application/pdf')

    blank_lines(1)

    # #BeeWell pupil video
    st.subheader('Introduction to the survey')
    st.markdown('''
    If you're unfamiliar with the #BeeWell survey or would like a reminder, you can
    check out the video below. This video (which was designed for pupils) explains
    what pupils could expect from taking part in the survey. For more information,
    see the 'About' page of the dashboard.
    ''')
    st.video('https://youtu.be/jmYH7F2Bd4Q')