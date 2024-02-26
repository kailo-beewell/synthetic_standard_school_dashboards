import streamlit as st
from kailo_beewell_dashboard.page_setup import page_setup, page_footer
from kailo_beewell_dashboard.authentication import check_password
from kailo_beewell_dashboard.stylable_container import header_container
from kailo_beewell_dashboard.reuse_text import reuse_text

# Set page configuration
page_setup('standard')

if check_password():

    # Page title
    st.title('About')

    # Subheader
    st.markdown(reuse_text['about_intro'])

    # Expand toggle
    expand = st.toggle('Toggle to expand all the boxes below', value=False)

    header_container('green_container', '🌿 Kailo', '#D9ECCA')
    with st.expander('What is Kailo?', expanded=expand):
        st.markdown(reuse_text['kailo'])
        st.image('images/kailo_systems_adapted.png')

    header_container('orange_container', '🐝 The #BeeWell survey', '#F7DCC8')
    with st.expander('Who took part in the #BeeWell survey in Devon?',
                     expanded=expand):
        st.markdown('''
This year, pupils in Years 8 and 10 at **seven secondary schools** from across
North Devon and Torridge completed the standard version of the #BeeWell survey.

A symbol version of the survey was also completed by pupils in Years 7 to 11
from **two non-mainstream schools** in Northern Devon.''')
        st.image('images/northern_devon.png')

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
* 🧑‍🤝‍🧑 **Relationships** - talking about feelings, acceptance, school
connection, support from staff, support from parents/carers, experiences of
discrimintation, support from friends, relative wealth and bulllying
* 🏠 **Environment** - feelings about home and local area, including future work
and education opportunities, and climate change
* 👨‍👩‍👧‍👦 **Demographics and experiences** - gender, transgender, sexual
orientation, neurodivergence, family background, care experience and young
carers''')

    with st.expander('How was the survey designed?', expanded=expand):
        st.markdown('''
The survey delivered in Northern Devon was adapted from the first #BeeWell
survey in Greater Manchester. That survey was developed through engagements
with over 150 young people from 15 different schools to understand what
wellbeing means to young people, what influences their wellbeing, and what
makes them thrive.

In Devon, we have adapted the survey to help it reflect the
priorities of young people in this area. Topics were based on conversations
across North Devon and Torridge with 195 young people and over 100 local actors
including: system leaders, practitioners, and people at 45 organisations
working with young people and broader communities. We have spoken with young
people and school staff in Northern Devon, as well as researchers and public
health professionals, amongst others, to choose, adapt and/or develop
appropriate questions for the survey. We'd like to extend our thanks to
everyone who supported this process.''')
        st.image('images/canva_people.png')

    with st.expander('Where else have these surveys been completed?',
                     expanded=expand):
        st.markdown('''
#BeeWell surveys have also been completed by pupils at schools in Hampshire,
Greater Manchester, the London borough of Havering, and Milton Keynes.

In 2023-24, **over 38,000 young people** completed a survey, with **nearly 300
schools** having now taken part in #BeeWell.

You can find out more about other sites at
https://beewellprogramme.org/.''')
        st.image('images/beewell_map.png')

    header_container('blue_container', '📊 Dashboard', '#D0C9FF')

    with st.expander('What data has been used in this dashboard?',
                     expanded=expand):
        st.markdown('''
This dashboard presents the results from pupils at your school who completed
the survey. To give context to these results, we've added comparisons against
pupils from schools across Northern Devon.

The survey responses were combined with data shared by the local authority such
as free school meal eligibility and special education needs to give further
insight into responses.''')

    with st.expander('How should we use these results?', expanded=expand):
        st.markdown(reuse_text['how_to_use_results'])
        st.image('images/thinking.png')

    with st.expander('Can I access this dashboard on different devices?',
                     expanded=expand):
        st.markdown(reuse_text['view_devices'])
        st.image('images/devices.png')

    with st.expander('''
Will there be support available for interpreting and actioning on the dashboard
results?''', expanded=expand):
        st.markdown(reuse_text['dashboard_support'])

    header_container('yellow_container', '😌 Wellbeing', '#FFF3B3')

    with st.expander('''
What do we already know about young people's wellbeing?''', expanded=expand):
        st.markdown(reuse_text['wellbeing_context'], unsafe_allow_html=True)

    page_footer(st.session_state.school)
