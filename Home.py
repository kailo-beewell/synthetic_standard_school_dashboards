import pandas as pd
import streamlit as st
from PIL import Image
from utilities.switch_page_button import switch_page
from utilities.fixed_params import page_setup, page_footer

# Set page configuration
page_setup()

# Import data used on this page
data = pd.read_csv('data/survey_data/aggregate_scores.csv')

###############################################################################

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
* **About** - Read information on the #BeeWell survey, Kailo, and this dashboard
* **Summary** - See a simple overview of results from pupils at your school, compared
with other schools
* **Explore results** - Explore how your pupils responded to each survey
question, and see further information on how the summary page's comparison to
other schools was generated
* **Who took part** - See the characteristics of the pupils who took part in the
survey
''')

# Blank space
st.text('')

# #BeeWell pupil video
st.subheader('Introduction to the survey')
st.markdown('''
If you're unfamiliar with the #BeeWell survey or would like a reminder, you can
check out the video below. This video (which was designed for pupils) explains
what pupils could expect from taking part in the survey. For more information,
see the 'About' page of the dashboard.
''')
st.video('https://youtu.be/jmYH7F2Bd4Q')

page_footer()