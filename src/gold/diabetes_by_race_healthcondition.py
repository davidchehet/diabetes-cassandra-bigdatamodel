from ..config import get_session
from ..utils import get_query_by_tag, check_race, check_health_condition
from cassandra.query import BatchStatement
import pandas as pd

session = get_session()
if session:
    print('Connected!')
else:
    print('Error occurred')

# Create our aggregated table in cassandra
session.execute(get_query_by_tag('src/cql_scripts/gold_scripts.cql', 'CREATE_GOLD_DIAB_BY_RACE_AND_HEALTH_CONDITION'))

# Select our race information from silver
rows = session.execute(get_query_by_tag('src/cql_scripts/gold_scripts.cql', 'SELECT_RACE_HEALTH'))

df = pd.DataFrame(list(rows))
batch = BatchStatement()

# Unique feature creation for this aggregation
df['race'] = df.apply(check_race, axis=1)
df['condition_group'] = df.apply(check_health_condition, axis=1)

# Calculate the prevalence of diabetes by race and condition group
diabetes_by_race_condition = df.groupby(['race', 'condition_group'])['diabetes'].mean()

# Insert query
insert_query = session.prepare(get_query_by_tag('src/cql_scripts/gold_scripts.cql', 'INSERT_INTO_RACE_HEALTH_TABLE'))

for(race, condition), prevalence in diabetes_by_race_condition.items():
    batch.add(insert_query,(race, condition, prevalence))

if batch:
    session.execute(batch)

print("Uploaded data")

session.shutdown()