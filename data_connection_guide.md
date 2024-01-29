# Guide on connection to data source

The datasets used to produced the dashboard will technically be anonymised data, but we do not want them to be easily downloadable and stored directly in the GitHub repository. Therefore, we have to connect to an external data source.

Below are **step-by-step guides on how to set up connection with data source**... (presently a few as explore different options and take notes on how it goes).

## TiDB Cloud

1. Add **mysqlclient** and **SQLAlchemy** to requirements.txt and update environment. In order to install mysqlclient on Linux, as on the mysqlclient [GitHub page](https://github.com/PyMySQL/mysqlclient), I had to first run `sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config`
2. Create a TiDB Cloud account, signing up with the Kailo BeeWell DSDL Google account
4. You'll have Cluster0 automatically created and in account. Click on the cluster, then go to Data > Import and drag and drop a csv file. Location will be Local as we upload from our computer. Set the database (synthetic_standard_survey) and table name (overall_counts).
    * Initially this failed when counts was set as DOUBLE value - changed to VARCHAR (512) and it was sucessfully
    * If you want to delete the data currently there (e.g. if incorrect or updating), go to Chat2Query and run `USE synthetic_standard_survey;` and `DROP TABLE tablename;`
4. Go to cluster overview and click the "Connect" blue button in the top right corner
5. On the pop-up, click "Generate Password". Make a record of that password
6. Copy the password and parameters from that pop-up into the .streamlit/secrets.toml file - example:
```
[connections.tidb]
dialect = "mysql"
host = "<TiDB_cluster_host>"
port = 4000
database = "<TiDB_database_name>"
username = "<TiDB_cluster_user>"
password = "<TiDB_cluster_password>"
```
9. On the Python streamlit page run:
```
conn = st.connection('tidb', type='sql')
df = conn.query('SELECT * from mytablename;')
```

## MongoDB

**Incomplete - requires you to install software to upload data**

### Set up with sample data

On MongoDB site:
1. Create MongoDB account - https://account.mongodb.com/account/register - using Kailo BeeWell DSDL Google account
2. On start up, deploy M0 free forever database (512 MB storage, shared RAM, shared vCPU) - using AWS, eu-west-1 Ireland, cluster kailo
3. Created a user
4. Set connection from My Local Environment and add my IP address (done automatically)
5. Navigated to Database Deployments page, clicked on the cluster name (kailo), selected the "collections" tab
6. Select load sample dataset

On Python:
1. Add pymongo (4.6.1) to requirements.txt and re-installed
2. Create .streamlit/secrets.toml with contents:
```
db_username = '<username>'
db_pswd = '<password>'
cluster_name = '<clustername>'
```
3. In the Python streamlit pages, add this code:
```
from pymongo import MongoClient

# Initialise connection, using cache_resource() so we only need to run once
@st.cache_resource()
def init_connection():
    return MongoClient(f'''mongodb+srv://{st.secrets.db_username}:{st.secrets.db_pswd}@{st.secrets.cluster_name}.2ebtoba.mongodb.net/?retryWrites=true&w=majority''')

client = init_connection()

@st.cache_data(ttl=60)
def get_data():
    db = client.sample_guides #establish connection to the 'sample_guide' db
    items = db.planets.find() # return all result from the 'planets' collection
    items = list(items)        
    return items
data = get_data()

st.markdown(data[0])
```

### Switching to using our data

Options for import of CSV data to MongoDB:
* MongoDBCompass
* mongoimport tool
* MongoDB Shell
* MongoDB Drivers

All require you to install software though.

## Firestore

**Incomplete - requires installation of paid software to upload documents or iterating over files which seems needlessly complex**

1. Add google-cloud-firestore==2.14.0 to requirements.txt and remake environment
2. Sign in to kailobeewell DSDL google account
3. Go to https://console.firebase.google.com/ and click "Create project"
4. Project name "kailo-synth-standard-school", accepted terms, disabled google analytics
5. Click on "Cloud Firestore", then "create a database"
6. Set location of europe-west2 (London) and start in test mode (open, anyone can read/write, will change later)
7. There is not anyway to import data using the Firebase console - https://medium.com/@xathis/import-csv-firebase-firestore-without-code-gui-tool-3987923947b6 - appears you have to install seperate software or write a script that parses the file, iterates over rows and careates document

## Private Google Sheet

**Incomplete - requires Google Cloud account**

I have used private Google sheets following this tutorial: https://docs.streamlit.io/knowledge-base/tutorials/databases/private-gsheet. I have also explained each step below.

1. Add st-gsheets-connection 0.0.3 to the Python environment (I found dependency incompatability with latest versions of pandas and geopandas, so I had to downgrade both - geopandas to 0.14.2 and pandas to 1.5.3).
2. If not already, add your data to Google Sheets.
3. If not already, create an account on the Google Cloud Platform and login (https://cloud.google.com/). We'll use the google cloud storage and google sheets API which are both available on the free tier.
4. Go to the APIs & Services dashboard.

## Deta Space

**Incomplete - requires developer mode**

- On Horizon, click the purple circle > add card to horizon > shortcut > collections and drag onto space
- Open Collections app and then create a new collection
- On that collection, go to collection settings then create new data key button, give the key a name, and click generate
- Requires developer mode, had to complete questionnaire and request it