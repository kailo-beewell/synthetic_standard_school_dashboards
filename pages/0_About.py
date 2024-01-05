import streamlit as st
from utilities.fixed_params import page_setup, page_footer
import base64
from pathlib import Path

# Set page configuration
page_setup()

# Page title
st.title('About')

st.header('The #BeeWell survey')
st.markdown('''
This year, pupils in Years 8 and 10 at seven secondary schools from across
North Devon and Torridge completed the standard version of the #BeeWell survey.  
            
The survey contained questions to measure wellbeing and the factors that might
impact it. To find out more about how the survey was developed and the questions
asked, click the button below:''')

with st.expander('What topics did the survey cover?'):
    st.markdown('''
The survey contained questions to measure wellbeing and the factors that might
impact it. Survey topics included:
* **Feelings about life** - autonomy, life satisfaction, optimism
* **Thoughts and feelings about self** - psychological wellbeing, 
self-esteem, stress, feelings around appearance
* **Feeling down** - negative affect, loneliness, supporting own wellbeing
* **Health and routines** - sleep, physical activity
* **Free time** - social media use, places to go and things to do
* **Relationships** - talking about feelings, acceptance, school connection,
support from staff, support from parents/carers, experiences of discrimintation,
support from friends, relative wealth and bulllying
* **Environment** - feelings about home and local area, including future work
and education opportunities, and climate change
* **Demographics and experiences** - gender, transgender, sexual orientation,
neurodivergence, family background, care experience and young carers
''')

# Create download button for PDF
# MIME type of data is not text/plain so set as below (since is bytes)
with open('./pdfs/survey_v21b.pdf', 'rb') as pdf_file:
    PDFbyte = pdf_file.read()
st.download_button(label='Download PDF about survey design and questions',
                    data=PDFbyte,
                    file_name='standard_beewell_survey_v2_1_b.pdf',
                    mime='application/octet-stream')

st.markdown('''
#BeeWell surveys were also completed by pupils at schools in Hampshire, Greater
Manchester and Havering. You can find out more about other sites at 
https://beewellprogramme.org/.''')

st.text('')
st.header('Kailo')
st.markdown('https://kailo.community/')

st.markdown('''
    Data information - will want to provide some details about calculations and
    data used within the dashboard, but likely finer details not necessary, and
    could instead be in a seperate document within the GitHub itself.''')


with st.expander('Release Notes'):
    st.markdown(Path('changelog.md').read_text(), unsafe_allow_html=True)

# Replace CSS styling of the buttons on this page
#st.markdown('''
#<style>
#div.stButton > button:first-child
#{
#    background-color: #D4ED6B;
#    border-color: #B0C74A;
#}
#</style>''', unsafe_allow_html=True)

st.text('')
st.text('')
st.subheader('FAQs')
with st.expander('Who completed the #BeeWell survey?'):
    st.markdown('''
This year, pupils in Years 8 and 10 at seven secondary schools from across
North Devon and Torridge completed the standard version of the #BeeWell survey.
The survey contained questions to measure wellbeing and the factors that might
impact it.
#BeeWell surveys were also completed by pupils at schools in Hampshire, Greater
Manchester and Havering. You can find out more at
''')
with st.expander('What is the purpose of the survey?'):
    st.markdown('Question answer')
with st.expander('How should we use these results?'):
    st.markdown('Question answer')
with st.expander('Can I access this dashboard on different devices?'):
    st.markdown('''
Yes - although it has been designed to view full screen on a computer/laptop, 
it is possible to view on other devices like a mobile phone. It will resize the 
page to your screen, but if the figures appear cramped/difficult to read, you may want to zoom out.''')

page_footer()