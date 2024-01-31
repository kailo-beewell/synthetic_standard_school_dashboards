# Guide on connection to data source

The datasets used to produced the dashboard will technically be anonymised data, but we do not want them to be easily downloadable and stored directly in the GitHub repository. Therefore, we have to connect to an external data source.

Below are **step-by-step guides on how to set up connection with data source**... (presently a few as explore different options and take notes on how it goes).

## TiDB Cloud

**Successfully implemented and currently used in this repository**

**Part 1. Set up TIDB Cloud**

1. If not already doing so, make sure that when saving the Python DataFrames to CSV files, you include `na_rep='NULL'` in `df.to_csv()`. Otherwise, you will encounter issues with SQL struggling to parse Python's null values.
2. Create a TiDB Cloud account - I used the Kailo BeeWell DSDL Google account
3. You'll have Cluster0 automatically created and in account. Click on the cluster, then go to Data > Import and drag and drop a csv file.
    * Location will be "Local" as we upload from our computer.
    * Set the database (synthetic_standard_survey) and table name (I chose to match filename e.g. overall_counts).
    * For **aggregate_responses** and **aggregate_responses_rag**, set **counts** and **percentages** columns to **VARCHAR(512)**. This means they are read as strings and ensures exact match to CSV (e.g. 0.0 rather than 0).
    * I found some unusual behaviour when replacing one of the tables, where using the same name as before, it was doing something (modifying order maybe, not clear) causing it to not match the CSV file - this was resolved by deleting the back-ups

**Part 2. Link Streamlit to TiDB Cloud**

I have used and explained two methods - one that only worked on my local machine, and one that worked both on my local machine and when deployed on Streamlit Community Cloud.

Method that is **compatible** with Streamlit Community Cloud:

1. Add **pymysql** to requirements.txt and update enviornment
2. On TiDB Cloud, go to the cluster overview and click the "Connect" blue button in the top right corner. On the pop-up, click:
    * "Generate Password" - make a record of that password
    * "Download the CA Cert" - to get the .pem file

3. Copy the password and parameters from that pop-up into the .streamlit/secrets.toml file - example:
```
[tidb]
dialect = 'mysql'
driver = 'pymysql'
host = '<TiDB_Host>'
port = '<TiDB_Port>'
database = '<TiDB_Database>'
username = '<TiDB_User>'
password = '<TiDB_Password>'
root_cert = '''<Copy of contents of .pem file>'''
```

4. Likewise copy this information into the deployed app's secrets. To do this, open https://share.streamlit.io/ and go to the Settings of dashboard, then click on the Secrets tab, and paste it into there.

5. To import the data within the Streamlit app, follow the code below. It is simpler to use pd.read_sql() instead of producing the get_df() function, but read_sql() returns an error message as we haven't set this up with SQLAlchemy - and so would likely need to modify connection so it is based on that and a connection string, rather than using pymysql.connect(), if we wanted to use read_sql().
```
from tempfile import NamedTemporaryFile
import pymysql

def get_df(query, conn):
    '''
    Get data from the connected SQL database

    Parameters:
    -----------
    query : string
        SQL query
    conn : connection object
        Connection to the SQL database

    Returns:
    --------
    df : pandas DataFrame
        Dataframe produced from the query
    '''
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(cursor.fetchall(), columns=columns)
    return df


# Create temporary PEM file for setting up the connection
with NamedTemporaryFile(suffix='.pem') as temp:

    # Write the temporary file
    temp.write(st.secrets.tidb.root_cert.encode('utf-8'))

    # Temporary file have pointer to current position in file - as we have
    # just written, the pointer is at the end of the last write, so if you
    # don't seek, you would read from the end of the file and find nothing
    temp.seek(0)

    # Set up connection manually, providing the temporary PEM file
    # (as cannot use st.connection() without providing tempfile name in secrets)
    conn = pymysql.connect(
        host = st.secrets.tidb.host,
        user = st.secrets.tidb.username,
        password = st.secrets.tidb.password,
        database = st.secrets.tidb.database,
        port = st.secrets.tidb.port,
        ssl_verify_cert = False,
        ssl_verify_identity = False,
        ssl_ca = temp.name
    )

    scores = pd.get_df('SELECT * FROM aggregate_scores;', conn)
```

Method that was **not** compatible with Streamlit Community Cloud (due to issues with environment not being built due to mysqlclient):

1. Add **mysqlclient** and **SQLAlchemy** to requirements.txt and update environment. In order to install mysqlclient on Linux, as on the mysqlclient [GitHub page](https://github.com/PyMySQL/mysqlclient), I had to first run `sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config`
2. As above, get the password and details for the secrets file, but this time structured differently:
```
[connections.tidb]
dialect = "mysql"
host = "<TiDB_cluster_host>"
port = 4000
database = "<TiDB_database_name>"
username = "<TiDB_cluster_user>"
password = "<TiDB_cluster_password>"
```

3. To import the data within the Streamlit app:
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