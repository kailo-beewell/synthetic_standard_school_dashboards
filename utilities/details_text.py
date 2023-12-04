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

        'stress': '''
**Question:** Pupils were asked how often the felt the following statements in the last month.  \n
**Interpretation:** From left to right, responses range from:  
* 'Never' - Feeling **more stressed** and struggling to cope, to  
* 'Very Often' - Feeling **less stressed** and better able to cope''',

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