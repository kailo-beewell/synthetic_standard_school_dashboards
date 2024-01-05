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
<p style='text-align: center;'>
Thank you for taking part in the #BeeWell survey delivered by Kailo.<br>
You can use this dashboard to explore results from pupils at your school.</p>
''', unsafe_allow_html=True)

# Image
st.image('images/home_image_3_transparent.png', use_column_width=True)

# Navigation
st.subheader('Navigation')
st.markdown('''
Use the sidebar on the left to navigate to different pages of the dashboard:
* **About** - Information on the #BeeWell survey, Kailo, and this dashboard
* **Summary** - Simple overview of your results compared with other schools
* **Explore results** - Explore how pupils responded to each survey question,
and see further information on how the summary page's comparison to other
schools was generated
* **Who took part** - Characteristics of the pupils who took part in the survey
''')

# Blank space
st.text('')

# Navigation video
st.subheader('Video guide')
st.video('https://youtu.be/jmYH7F2Bd4Q')
st.markdown('*Placeholder survey video - but I could screen record navigating dashboard?*')

page_footer()