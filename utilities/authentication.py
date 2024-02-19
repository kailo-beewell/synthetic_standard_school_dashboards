'''
Helper functions for user authentication
'''
import streamlit as st
import os
from django.core.wsgi import get_wsgi_application
from django.contrib.auth import authenticate

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()


def get_school(username):
    '''
    Finds the school based on the username

    Parameters
    ----------
    username : string
        Django username
    '''
    schools = {
        'schoola': 'School A',
        'schoolb': 'School B',
        'schoolc': 'School C',
        'schoold': 'School D',
        'schoole': 'School E',
        'schoolf': 'School F'
    }
    return schools[username]


def password_entered():
    '''
    Checks whether a password entered by the user is correct
    '''
    # Use Django to check if the username and password match record
    user = authenticate(
        username=st.session_state['username'],
        password=st.session_state['password']
        )
    # If this succeeds, delete the username and password, and keep record
    # of the user and school in the session state
    if user is not None:
        st.session_state['password_correct'] = True
        del st.session_state['password']
        del st.session_state['username']
        st.session_state.user = user
        st.session_state['school'] = get_school(str(user))
    else:
        st.session_state['password_correct'] = False


def login_screen():
    '''
    Produces message that is displayed on the login screen.
    '''
    st.title('The #BeeWell survey')
    st.markdown('''
Please enter your school username and password to login to the dashboard.

For this synthetic dashboard, we have six schools - choose a username and
password from the following:
* '**schoola**' and '**schoolapassword**' - n<10 for some demographic responses
* '**schoolb**' and '**schoolbpassword**' - no SEN
* '**schoolc**' and '**schoolcpassword**'
* '**schoold**' and '**schooldpassword**'
* '**schoole**' and '**schoolepassword**'
* '**schoolf**' and '**schoolfpassword**' - no Year 10s
''')


def check_password():
    '''
    Function that returns 'True' if the user has entered the correct password
    Stores the user to the session state, and finds the school's full name,
    and adds that to the session state as well.
    '''
    # If have not yet logged in...
    if 'password_correct' not in st.session_state:
        # Show inputs for username and password
        login_screen()
        st.text_input('Username', key='username')
        st.text_input('Password', type='password', key='password')
        st.write('')
        st.button(label='Enter', on_click=password_entered)
        return False
    elif not st.session_state['password_correct']:
        # Password not correct, show input boxes again and an error message
        login_screen()
        st.text_input('Username', key='username')
        st.text_input('Password', type='password', key='password')
        st.write('')
        st.button(label='Enter', on_click=password_entered)
        st.error('😕 User not known or password incorrect')
        return False
    else:
        # Password correct.
        return True
