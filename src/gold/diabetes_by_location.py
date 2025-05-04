from ..config import get_session
from ..utils import get_query_by_tag
from cassandra.query import BatchStatement
import pandas as pd

session = get_session()
if session:
    print('Connected!')
else:
    print('Error occurred')

# Create gold table
session.execute(get_query_by_tag('src/cql_scripts/gold_scripts.cql', 'CREATE_LOC_TABLE'))

# Source location info from silver table
rows = session.execute(get_query_by_tag('src/cql_scripts/gold_scripts.cql', 'SELECT_LOC_INFO_SILVER'))

df = pd.DataFrame(list(rows))
batch = BatchStatement()

diabetes_by_location = df.groupby(['location'])['diabetes'].mean()

insert_query = session.prepare(get_query_by_tag('src/cql_scripts/gold_scripts.cql', 'INSERT_INTO_LOC'))

for (location), prevalence in diabetes_by_location.items():
    batch.add(insert_query, (location, prevalence))

if batch:
    session.execute(batch)

print("Uploaded data")

session.shutdown()