# 🐝 Synthetic standard school dashboards

Dashboards for schools who completed the standard #BeeWell survey in 2023/24. 🏫

These are created using completely random synthetic data, so this repository is public, as it contains no project data. The prototypes will be used to create official dashboards using actual school data after data collection.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://synthetic-beewell-kailo-standard-school-dashboard.streamlit.app/)

Streamlit Community Cloud only appears to work with virtual environment (states compatability with environment.yml but failed), so we use a virtual environment with the requirements.txt file provided and python version 3.9.12 (with community cloud set up on python 3.9).

Manage streamlit apps here: https://share.streamlit.io/. To push changes to the app from main, go that site and select 'reboot' (won't implement changes automatically from main).

User authentication is managed using **Django** - learn more about this from the `authentication_guide.md`.

The data for the application is stored in and pulled from ***TiDB Cloud*** (as this is the synthetic dashboard, you'll also find copies of the CSV files uploaded to TiDB Cloud in the "data/survey_data" folder) - learn more about this from the `data_connection_guide.md`.

## Tips for working on the dashboards

To set up environment on your machine, need pip + python + virtualenv + virtualenvwrapper installed. Use of virtualenvwrapper will ensure that all your environments are stored in one location rather than in random folders, making it easier to find them. Commands required when working with environment:
* Create environment - `mkvirtualenv env_kailo_dashboards`
* Enter environment -  `workon env_kailo_dashboards`
* Install requirements into environment - `pip install -r requirements.txt`
* See list of all available environments - `workon`
* List contents of active environment - `pip list`
* Delete environment - `rmvirtualenv env_kailo_dashboards`

Formatting:
* Lint .py files using the Flake8 VSCode extension
* Function docstrings use numpy docstring [style guide](https://numpydoc.readthedocs.io/en/latest/format.html)