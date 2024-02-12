'''
Function to create dictionaries with text that accompanies figures.
'''


def create_response_description():
    '''
    Creates and returns dictionary with descriptions for the survey responses

    Returns
    -------
    stacked_descrip : dictionary
        Keys are variables and sub-groups of variables, and values are
        descriptions to be displayed above the charts.
    '''
    stacked_descrip = {
        'autonomy': '''
For these questions, pupils were asked to think about how each statement
relates to their life, and then indicate how true it is for them.''',

        # 'life_satisfaction': '''''',

        'optimism_future': '''
In this first question, pupils were asked how often they feel optimistic about
their future.''',

        'optimism_other': '''
In the following questions, pupils were asked to choose how much they feel each
statement describes themselves.''',

        'wellbeing': '''
For these questions, some statements about feelings and thoughts were provided.
Pupils were asked to choose the response that best describes their experience
of each over the last 2 weeks.''',

        'esteem': '''
Pupils were told that these questions ask about their current feelings about
themselves. They were asked to choose the answers that best describe how
strongly they agree or disagree with each of the statements about themselves
now.''',

        'stress': '''
Pupils were told that these questions about about their feelings and thoughts
during the last month. In each case, they were asked to choose how often they
felt or thought a certain way.''',

        # 'appearance_happy': '''''',

        # 'appearance_feel': '''''',

        'negative': '''
For these questions, there were statements about how pupils feel. They were
asked to choose the answer that was best for them.''',

        # 'lonely': '''''',

        'support': '''
Pupils were asked how strongly they agree or disagree with the following
statements.''',

        # 'sleep': '''''',

        'physical_days': '''
Young people were told that this question was about their physical
activity. It stated that we were 'particularly interested in activity that
increases your heart rate and makes you get out of breath some of the time.
Physical activity can be done in sports, school activities, playing with
friends, or walking and cycling to school or other places.' They were then
asked how often they do physical activity.
''',

        'physical_hours': '''
Young people were asked to think about the days when they are physically
active, and to think about all the different activities they typically do over
the course of the day. They were then asked how long they normally spend doing
physical activity
''',

        # 'free_like': '''''',

        'media': '''
For this question, young people were asked how many hours they would normally
spend on social media per day, with examples of sites or apps like TikTok,
Instagram, and Snapchat.''',

        # 'places_freq': '''''',

        'places_barriers': '''
Pupils were asked if there are any reasons that prevent them from doing
activities or going to places that they want to in their free time. They were
asked to select all that apply.
''',

        'talk_yesno': '''
Pupils were asked if they had ever talked with the following people about
feeling down (e.g. stressed, sad, anxious).
''',

        'talk_listen': '''
For pupils who responded yes, they were then asked if they felt listened to.
''',

        'talk_helpful': '''
For pupils who responded yes, they were also asked if the person provide
advice that they found helpful.
''',

        'talk_if': '''
For pupils who responded no, they were asked how they would feel about
speaking with that person when feeling down.
''',

        'accept': '''
Pupils were asked "**do you feel accepted as you are**" by the following
people.
''',

        # 'school_belong': '''''',

        # 'staff_relationship': '''''',

        # 'home_relationship': '''''',

        # 'home_happy': '''''',

        # 'local_safe': '''''',

        'local_other': '''
For these questions, pupils were asked to choose the answer that best
describes how strongly they agree or disagree with the statements about where
they live.
''',

        # 'discrim': '''''',

        # 'belong_local': '''''',

        # 'wealth': '''''',

        'future_options': '''
Pupils were told that these questions are about **future options for work,
education and training in their local area.** We explained that this might
include jobs, apprenticeships, college courses, university courses.
''',

        # 'future_interest': '''''',

        # 'future_support': '''''',

        # 'climate': '''''',

        # 'social': '''''',

        # 'bully': ''''''

        # Several demographic question have no description provided

        'transgender': '''
For this question, pupils were told that some young people are transgender,
and that this means  that their gender is different to the one they were
assigned at birth (e.g.,  someone who was assigned male at birth but is a girl,
or someone who is non-binary and is not a girl or a boy). They were then asked
whether they consider themselves to be transgender.
''',

        'sen': '''
Provide description of the SEN data once I am aware of exactly what it is based
on (e.g. EHCP). This information is provided by Devon County Council.
''',

        'neurodivergent': '''
Pupils were told that this question is about identifying as neurodivergent.
They were told that being neurodivergent can mean being:

* Dyslexic
* Dyspraxic
* Dyscalculic
* Autistic

Or having:

* ADHD or ADD
* A tic disorder such as Tourette’s
* A speech, language or communication disorder
* An intellectual disability or learning disability
* Dysgraphia
* Foetal alcohol spectrum disorder

It stated that they might describe themselves as neurodivergent if they
identify with one or more of the conditions above, or they may be waiting for
or have a diagnosis. They were then asked if they identify as neurodivergent.
''',

        'birth_parent1': '''
These questions were about the background of pupils and their parents
(specifically, if they were born in or came to the UK).
'''
        }

    return stacked_descrip
