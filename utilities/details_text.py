'''
Functions to create and return dictionaries containing text for the Details
page, to help minimise the amount of information on that .py file
'''

def create_stacked_descrip():
    '''
    Creates and returns dictionary with descriptions for the stacked bar charts
    '''
    stacked_descrip = {
        'autonomy': '''
**Question:** Pupils were asked to think about how each statement relates to their life, and then indicate how true it is for them.  
**Interpretation:** From left to right, responses range from feeling **less** in control ('1 - Completely not true') to **more** in control ('5 - Completely true').''',

        'life_satisfaction': '''
**Interpretation:** From left to right, responses range from feeling **less** satisfied ('0 - not at all') to **more** satisfied ('10 - completely').''',

        'optimism_future': '''
**Question:** How often pupils feel optimistic about the future.  
**Interpretation:** From left to right, responses range from feeling **less** optimistic ('Almost never') to **more** optimistic ('Always').''',

        'optimism_other': '''
**Question:** How much pupils feel the following statements to describe themselves.  
**Interpretation:** From left to right, responses range from feeling **less** optimistic ('Not at all like me') to **more** optimistic ('Very much like me').''',

        'wellbeing': '''
**Question:** Pupils were asked to choose the response that best describes their experience of the following statements over the last 2 weeks.  \n
**Interpretation:** From left to right, responses range from:
* 'None of the time' = **lower** wellbeing levels, to  
* 'All of the time' = **higher** wellbeing levels''',

        'esteem': '''
**Question:** Pupils were asked how strongly they agreed or disagreed with the following statements about themselves now.  \n
**Interpretation:** From left to right, responses range from:
* 'Strongly disagree' = **lower** levels of self-esteem
* 'Strongly agree' = **higher** levels of self-esteem''',

        'stress': '''
**Question:** Pupils were asked how often they felt/thought the following statements during the last month.  \n
**Interpretation:** From left to right, responses range from:
* 'Never' = Feeling **more** stressed and struggling to cope, to  
* 'Very Often' = Feeling **less** stressed and better able to cope''',

        'appearance_happy': '''
**Interpretation:** From left to right, responses range from:
* '0 - Very unhappy'
* '10 - Very happy'  \n
Pupils were also able to respond 'prefer not to say'.''',

        'appearance_feel': '''
**Interpretation:** From left to right, responses range from:
* 'Strongly agree' = appearance **absolutely** affects how feel about self
* 'Strongly disagree' = appearance **does not** affect how feel about self''',

        'negative': '''
**Question:** Pupils were asked which answer was best for them for the following statements about how they feel.  \n
**Interpretation:** From left to right, responses range from:
* 'Always' = **more** experience of emotional difficulties
* 'Never' = **less** experience of emotional difficulties''',

        'lonely': '''
**Interpretation:** From left to right, responses range from:
* 'Often or always' = **more** lonely
* 'Never' = **less** lonely''',

        'support': '''
**Question:** Pupils were asked how strongly they agree or disagree with the following statements.  \n
**Interpretation:** From left to right, responses range from:
* 'Strongly disagree' = **less** knowledge on supporting themselves and finding advice
* 'Strongly agree' = **more** knowledge on supporting themselves and finding advice''',

        'sleep': '''''',

        'physical_days': '''
**Question:** Young people were told that this question was about their physical \
activity. It stated that we were 'particularly interested in activity that \
increases your heart rate and makes you get out of breath some of the time. \
Physical activity can be done in sports, school activities, playing with \
friends, or walking and cycling to school or other places.'  
**Interpretation:** From left to right, responses range from **less** to **more** days of physical activity per week.
''',

        'physical_hours': '''
**Question:** Young people were asked to think about the days when they are \
physically active, and to think about all the different activities they \
typically do over the course of the day - and were then asked the following question.  
**Interpretation:** From left to right, responses range from **shorter** to **longer** amounts of time spend doing physical activity.
''',

        'free_like': '''
**Interpretation:** From left to right, responses range from:
* 'Almost never' = **less** able to do things they like in their free time
* 'Almost always' = **more** able to do things they like in their free time
''',

        'media': '''
**Question:** Young people were asked how many hours they would normally spend \
on social media per day, with examples of sites or apps like TikTok, Instagram, and Snapchat.  
**Interpretation:** Responses range from **7+ hours** per day to **0 hours** per day.''',

        'places_freq': '''''',

        'places_barriers': '''
**Question:** Pupils were asked if there are any reasons that prevent them \
from doing activities or going to places that they want to in their free time. \
They were asked to select all that apply.
''',

        'home_happy': '''
This question is about how happy young people are with the home they live in.  
Young people were ask to rate their response on a scale of 0 to 10, where 0 is very unhappy, 5 is neither happy or unhappy, and 10 is very happy''',

        'bully': '''
These questions are about the frequency with which young people experience different types of bullying. \
They were asked about three types of bullying, and given the following definitions for each:  
* Being physically bullied at school - by this we mean getting hit, pushed around, threatened, or having belongings stolen.  
* Being bullied in other ways at school - by this we mean insults, slurs, name \
calling, threats, getting left out or excluded by others, or having rumours spread about you on purpose  
* Being cyber-bullied - by this we mean someone sending mean text or online \
messages about you, creating a website making fun of you, posting pictures that make you look bad online, or sharing them with others.'''
        }
    
    return(stacked_descrip)