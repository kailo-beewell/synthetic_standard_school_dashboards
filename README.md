# 🐝 Synthetic standard school dashboards

Dashboards for schools who completed the standard #BeeWell survey in 2023/24. 🏫

These are created using completely random synthetic data, so this repository is public, as it contains no project data. The prototypes will be used to create official dashboards using actual school data after data collection.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://synthetic-beewell-kailo-standard-school-dashboard.streamlit.app/)

Streamlit Community Cloud only appears to work with virtual environment (states compatability with environment.yml but failed), so we use a virtual environment with the requirements.txt file provided and python version 3.9.12 (with community cloud set up on python 3.9). To set up environment, need pip + python + virtualenv installed, then run:
* Create environment - `virtualenv kailo_dashboards`
* Enter environment -  `source kailo_dashboards/bin/activate`
* Install requirements into environment - `pip install -r requirements.txt`
* Delete environment - `deactivate` then `rm -r kailo_dashboards`
* List packages in environment - `pip list`

Manage streamlit apps here: https://share.streamlit.io/. To push changes to the app from main, go that site and select 'reboot' (won't implement changes automatically from main).

User authentication is managed using **Django** - learn more about this from the `authentication_guide.md`.

The data for the application is stored in and pulled from ***TiDB Cloud*** (as this is the synthetic dashboard, you'll also find copies of the CSV files uploaded to TiDB Cloud in the "data/survey_data" folder) - learn more about this from the `data_connection_guide.md`.