import streamlit as st
from utilities.page_setup import page_setup, blank_lines
from utilities.authentication import check_password
from utilities.import_data import import_tidb_data
from utilities.static_report import create_static_report
import weasyprint
from tempfile import NamedTemporaryFile

# Set page configuration
page_setup()

if check_password():

    # Import the data from TiDB Cloud if not already in session state
    import_tidb_data()

    # Add name of school (to help with monitoring)
    st.markdown(st.session_state.school)

    # Title and introduction
    st.title('The #BeeWell Survey')
    st.markdown('''
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
* **About** - Read information on the #BeeWell survey, Kailo, and this
dashboard
* **Summary** - See a simple overview of results from pupils at your school,
compared with other schools
* **Explore results** - Explore how your pupils responded to each survey
question, and see further information on how the summary page's comparison to
other schools was generated
* **Who took part** - See the characteristics of the pupils who took part in
the survey''')

    blank_lines(2)

    # Section for downloading PDF report
    st.subheader('Download PDF report')
    st.markdown('''
You can use the interactive dashboard to explore results for your school. We
also provide the option of downloading a PDF version of your results below. You
can choose whether the report shows the results for all pupils, or whether it
provides a comparison of results between two pupil groups.''')

    # Choose comparator
    chosen_group = st.selectbox(label='In the report, show results:', options=[
        'For all pupils', 'By year group', 'By gender', 'By FSM', 'By SEN'])
    blank_lines(1)

    # Get group name with only first character modified to lower case
    group_lower_first = chosen_group[0].lower() + chosen_group[1:]
    # Get group name as lower case with no spaces
    group_file_string = chosen_group.lower().replace(' ', '_')

    # If report had not be generated, show generate report button
    if f'pdf_report_{group_file_string}' not in st.session_state:
        # If this button is clicked...
        if st.button(f'''Generate report {group_lower_first} - will take
                     around 30 seconds'''):
            # Show spinner whilst operation occurs
            with st.spinner('Generating report'):
                # Produce the HTML for the report
                st.session_state.html_content = create_static_report(
                    chosen_school=st.session_state.school,
                    chosen_group=chosen_group,
                    df_scores=st.session_state.scores_rag,
                    df_prop=st.session_state.responses,
                    counts=st.session_state.counts,
                    dem_prop=st.session_state.demographic,
                    pdf_title=f'''
#BeeWell Kailo School Report 2024 {group_lower_first}''')
                # Convert to temporary PDF file, then read PDF back into
                # environment and store report in the session state
                with NamedTemporaryFile(suffix='.pdf') as temp:
                    weasyprint.HTML(
                        string=st.session_state.html_content).write_pdf(temp)
                    temp.seek(0)
                    st.session_state[f'pdf_report_{group_file_string}'] = open(
                        temp.name, 'rb')
            # Re-run script, so the generate button is removed
            st.rerun()

    # If report has been generated for this group, show download button
    elif f'pdf_report_{group_file_string}' in st.session_state:
        st.download_button(
            label=f'''
Download report {group_lower_first}''',
            data=st.session_state[f'pdf_report_{group_file_string}'],
            file_name=f'kailo_beewell_school_report_{group_file_string}.pdf',
            mime='application/pdf')

    blank_lines(2)

    # #BeeWell pupil video
    st.subheader('Introduction to the survey')
    st.markdown('''
If you're unfamiliar with the #BeeWell survey or would like a reminder, you can
check out the video below. This video (which was designed for pupils) explains
what pupils could expect from taking part in the survey. For more information,
see the 'About' page of the dashboard.''')
    st.video('https://youtu.be/jmYH7F2Bd4Q')
