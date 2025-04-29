# CONNECT TO CASSANDRA + IMPORT UTIL FNs
from config import get_session
from utils import get_query_by_tag
import pandas as pd
import uuid as uuid

TABLE = 'bronze_level'
session = get_session()
if session:
    print('Connected!')
else:
    print('Error occurred')

# Create 'bronze_level' table in 'diabetes' keyspace
session.execute(get_query_by_tag('src/cql_scripts/bronze_scripts.cql', 'CREATE_BRONZE_LEVEL_TABLE'))

# Read in our csv with pandas
df = pd.read_csv('./diabetes.csv')
capacity = 0

for _, row in df.iterrows():
# Insert our csv into our 'bronze_level' table in keyspace 'diabetes'
    session.execute(get_query_by_tag('src/cql_scripts/bronze_scripts.cql', 'INSERT_RAW_DATA'),
                    (uuid.uuid4(), row['year'], row['gender'], row['age'], row['location'], row['race_AfricanAmerican'],
                     row['race_Asian'],row['race_Caucasian'], row['race_Hispanic'], row['race_Other'], row['hypertension'],
                     row['heart_disease'], row['smoking_history'], row['bmi'], row['hbA1c_level'], row['blood_glucose_level'],
                     row['diabetes'], row['clinical_notes'])
                    )
    if _ % 1000 == 0:
        capacity += 1
        print(f'{capacity}% Uploaded')
    

