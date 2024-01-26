# Authentication guide

This guide provides a step-by-step on how I set up the user authentication for this dashboard, which was based on these tutorials:
* https://towardsdatascience.com/secure-your-streamlit-app-with-django-bb0bee2a6519.
* https://towardsdatascience.com/streamlit-access-control-dae3ab8b7888

## How to set up user authentication

1. If not already in environment, install django (add to requirements.txt, recreate environment)
2. Create a Django app. In terminal: `django-admin startproject config .`. This produced a config folder containing 5 .py files.
3. Create a superuser to manage all other users: `python3 manage.py migrate` and `python3 manage.py createsuperuser`. Then enter user as `kailobeewell` and the dartington email address. I have record of password personally which I can share with other team members.
4. Start the server: `python3 manage.py runserver`.
5. Open web-browser and go to http://localhost:8000/admin/. Login with the superuser username and password just created.
6. Add some users by clicking '+ Add' next to Users, then entering a username and password for each user. For the synthetic dashboard, I create some basic logins (which need to be more secure for actual dashboard). For each user followed the format of:
    * Username: schoola
    * Password: schoolapassword
7. Created the authentication.py script (see utilities folder)
8. On each of the app pages, imported the check_password() function from authentication.py, then sat all the page code under it, eg:
```
import streatmlit as st
from utilities.authentication import check_password

if check_password():
    st.title('Page title')
    st.write('Page content)
    ...
```