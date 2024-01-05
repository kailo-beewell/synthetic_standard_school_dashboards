import streamlit as st
from utilities.fixed_params import page_setup, page_footer
import base64
from pathlib import Path

# Set page configuration
page_setup()

# Page title
st.title('About')

# Subheader
st.markdown('''
This page contains information about #BeeWell, Kailo and this dashboard.''')

# Divider image
st.text('')
st.image('images/circle_divider.png')

st.header('The #BeeWell survey')
with st.expander('Who took part in the #BeeWell survey in Devon?'):
    st.markdown('''
This year, pupils in Years 8 and 10 at seven secondary schools from across
North Devon and Torridge completed the standard version of the #BeeWell survey.
A symbol version of the survey was also completed by pupils in Years 7 to 11
from two non-mainstream schools in Northern Devon.''')
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
with st.expander('How was the survey designed?'):
    st.markdown('''
The survey delivered in Northern Devon was adapted from the first #BeeWell
survey in Greater Manchester. That survey was developed through engagements
with over 150 young people from 15 different schools to understand what
wellbeing means to young people, what influences their wellbeing, and what makes
them thrive. In Devon, we have adapted the survey to help it reflect the
priorities of young people in this area. Topics were based on conversations
across North Devon and Torridge with 195 young people and over 100 local actors
including: system leaders, practitioners, and people at 45 organisations
working with young people and broader communities. We have spoken with young
people and school staff in Northern Devon, as well as researchers and public
health professionals, amongst others, to choose, adapt and/or develop
appropriate questions for the survey. We'd like to extend our thanks to
everyone who supported this process.
''')
with st.expander('Where else have these surveys been completed?'):
    st.markdown('''
#BeeWell surveys were also completed by pupils at schools in Hampshire, Greater
Manchester and Havering. You can find out more about other sites at 
https://beewellprogramme.org/.''')

# Divider image
st.text('')
st.image('images/circle_divider.png')

st.header('Kailo')
with st.expander('What is Kailo?'):
    st.markdown('https://kailo.community/')

# Divider image
st.text('')
st.image('images/circle_divider.png')

st.header('Dashboard')
with st.expander('How should we use these results?'):
    st.markdown('Question answer')
with st.expander('Can I access this dashboard on different devices?'):
    st.markdown('''
Yes - although it has been designed to view full screen on a computer/laptop, 
it is possible to view on other devices like a mobile phone. It will resize the 
page to your screen, but if the figures appear cramped/difficult to read, you may want to zoom out.''')
with st.expander('eg How was stuff calculated?'):
    st.markdown('''
Data information - will want to provide some details about calculations and
data used within the dashboard, but likely finer details not necessary, and
could instead be in a seperate document within the GitHub itself.''')

# Divider image
st.text('')
st.image('images/circle_divider.png')

st.header('''Young people's wellbeing: what we already know''')
st.markdown('''
* The peak age of onset of mental health difficulties is 14.5 years.<sup>[1]</sup>
* Mental health and wellbeing in adolescence predicts adult health, labour
market and other important outcomes.<sup>[2]</sup>
* The wellbeing of adolescents has decreased in the last two decades, while the
prevalence of mental health difficulties among them has increased.<sup>[3,4]</sup>
* A recent international study ranked the UK’s young people fourth from bottom
across nearly 80 countries in terms of life satisfaction.<sup>[5,6]</sup>
* Young people’s mental health and wellbeing can be influenced by multiple
drivers, including their health and routines, hobbies and entertainment,
relationships, school, environment and society, and how they feel about their
future.<sup>[7]</sup>
''', unsafe_allow_html=True)

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

page_footer()