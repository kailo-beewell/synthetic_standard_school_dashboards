import streamlit as st
from utilities.fixed_params import page_setup
from utilities.stylable_container import stylable_container, header_container
import base64
from pathlib import Path

# Set page configuration
page_setup()

# Page title
st.title('About')

# Subheader
st.markdown('''
This page has lots of helpful information about the research projects (Kailo
and #BeeWell), as well as advice on using and accessing this dashboard, and
some background information around young people's wellbeing.''')

# Expand toggle
expand = st.toggle('Toggle to expand all the boxes below', value=False)


header_container('green_container', '🌿 Kailo', '#D9ECCA')

with st.expander('What is Kailo?', expanded=expand):
    st.markdown('''
Our aim is to help local communities, young people and public service partnerships better understand and address the root causes (and wider determinants) of young people’s mental health.

We’re made up of leading academics, designers and practitioners, dedicated to working alongside communities in specific localities. Together, we will test and co-design evidence-based responses (in a ‘framework’) to these root causes, over the next four years.

Our model is formed of three key stages:
* **Early Discovery** - here, we build strong and trusted relationships with
                local partners with an aim to understand what matters locally
                thus, forming communities around youth- and community-centred
                priorities
* **Deeper Discovery and Codesign** - this stage, which we're in currently,
                sees us codesign systemic responses to social determinants.
* **Prototyping, Implementation and Testing** - this is where the learning is applied, integrating the codesigned responses with the local system, prototyping them and making iterative refinements along the way.

To find our more about Kailo, check out our site: https://kailo.community/
''')

header_container('orange_container', '🐝 The #BeeWell survey', '#F7DCC8')

with st.expander('Who took part in the #BeeWell survey in Devon?', expanded=expand):
    st.markdown('''
This year, pupils in Years 8 and 10 at **seven secondary schools** from across
North Devon and Torridge completed the standard version of the #BeeWell survey.  
                
A symbol version of the survey was also completed by pupils in Years 7 to 11
from **two non-mainstream schools** in Northern Devon.''')

with st.expander('What topics did the survey cover?', expanded=expand):
    st.markdown('''
The survey contained questions to measure wellbeing and the factors that might
impact it. Survey topics included:
* 🌱 **Feelings about life** - autonomy, life satisfaction, optimism
* 🧍 **Thoughts and feelings about self** - psychological wellbeing, 
self-esteem, stress, feelings around appearance
* 😟 **Feeling down** - negative affect, loneliness, supporting own wellbeing
* 🧘‍♂️ **Health and routines** - sleep, physical activity
* 🕰️ **Free time** - social media use, places to go and things to do
* 🧑‍🤝‍🧑 **Relationships** - talking about feelings, acceptance, school connection,
support from staff, support from parents/carers, experiences of discrimintation,
support from friends, relative wealth and bulllying
* 🏠 **Environment** - feelings about home and local area, including future work
and education opportunities, and climate change
* 👨‍👩‍👧‍👦 **Demographics and experiences** - gender, transgender, sexual orientation,
neurodivergence, family background, care experience and young carers
''')

with st.expander('How was the survey designed?', expanded=expand):
    st.markdown('''
The survey delivered in Northern Devon was adapted from the first #BeeWell
survey in Greater Manchester. That survey was developed through engagements
with over 150 young people from 15 different schools to understand what
wellbeing means to young people, what influences their wellbeing, and what makes
them thrive.  

In Devon, we have adapted the survey to help it reflect the
priorities of young people in this area. Topics were based on conversations
across North Devon and Torridge with 195 young people and over 100 local actors
including: system leaders, practitioners, and people at 45 organisations
working with young people and broader communities. We have spoken with young
people and school staff in Northern Devon, as well as researchers and public
health professionals, amongst others, to choose, adapt and/or develop
appropriate questions for the survey. We'd like to extend our thanks to
everyone who supported this process.
''')
    st.image('images/canva_people.png')

with st.expander('Where else have these surveys been completed?', expanded=expand):
    st.markdown('''
#BeeWell surveys have also been completed by pupils at schools in Hampshire, 
Greater Manchester, the London borough of Havering, and Milton Keynes.  
                
In 2023-24, **over 38,000 young people** completed a survey, with **nearly 300
schools** having now taken part in #BeeWell.

You can find out more about other sites at 
https://beewellprogramme.org/.''')
    st.image('images/beewell_map.png')

header_container('blue_container', '📊 Dashboard', '#D0C9FF')

with st.expander('How should we use these results?', expanded=expand):
    st.markdown('Question answer')

with st.expander('Can I access this dashboard on different devices?', expanded=expand):
    st.markdown('''
Yes - although it has been designed to view full screen on a computer/laptop, 
it is possible to view on other devices like a mobile phone. It will resize the 
page to your screen, but if the figures appear cramped/difficult to read, you may want to zoom out.''')

with st.expander('eg How was stuff calculated?', expanded=expand):
    st.markdown('''
Data information - will want to provide some details about calculations and
data used within the dashboard, but likely finer details not necessary, and
could instead be in a seperate document within the GitHub itself.''')

header_container('yellow_container', '😌Wellbeing', '#FFF3B3')

with st.expander('''Young people's wellbeing: what we already know''', expanded=expand):
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

#with st.expander('Release Notes', expanded=expand):
#    st.markdown(Path('changelog.md').read_text(), unsafe_allow_html=True)

# Replace CSS styling of the buttons on this page
#st.markdown('''
#<style>
#div.stButton > button:first-child
#{
#    background-color: #D4ED6B;
#    border-color: #B0C74A;
#}
#</style>''', unsafe_allow_html=True)