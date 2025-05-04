# CONNECT TO CASSANDRA + IMPORT UTIL FNs
from config import get_session
from utils import get_query_by_tag, categorize_smoking_history, binarize_gender, format_location
from cassandra.query import BatchStatement
import pandas as pd
import uuid as uuid

TABLE = 'silver_level'
session = get_session()
if session:
    print('Connected!')
else:
    print('Error occurred')

# Create our silver table in 'diabetes' keyspace
session.execute(get_query_by_tag('src/cql_scripts/silver_scripts.cql', 'CREATE_SILVER_LEVEL_TABLE'))

# Select our bronze data <=== This is what makes this ELT
select_bronze = session.prepare(get_query_by_tag('src/cql_scripts/bronze_scripts.cql', 'SELECT_FOR_SILVER'))

# Insert our silver data
insert_silver = session.prepare(get_query_by_tag('src/cql_scripts/silver_scripts.cql', 'INSERT_CLEANSED_DATA'))

# Execute bronze select => only rows where bmi >= 12 and bmi <= 60
rows = session.execute(select_bronze)

# Batch
batch = BatchStatement()
batch_size = 100
processed_rows = 0

# Process each row and insert into silver_level table
for row in rows:

    # Cleans outliers in BMI and prevents select * 
    if row.bmi >= 12 and row.bmi <= 60:

        cleaned_smoking_history = categorize_smoking_history(row.smoking_history)
        cleaned_gender = binarize_gender(row.gender)
        cleaned_location = format_location(row.location)
        cleaned_age = int(row.age)

        batch.add(insert_silver, (
            row.patient_id,
            row.year,
            cleaned_gender,
            cleaned_age,
            cleaned_location,
            row.race_african_american,
            row.race_asian,
            row.race_caucasian,
            row.race_hispanic,
            row.race_other,
            row.hypertension,
            row.heart_disease,
            cleaned_smoking_history,
            row.bmi,
            row.hba1c_level,
            row.blood_glucose_level,
            row.diabetes
        ))
        processed_rows += 1

        if processed_rows % batch_size == 0:
            session.execute(batch)
            batch.clear()

if batch:
    session.execute(batch)

print("Data processing from Bronze to Silver layer complete.")
session.shutdown()
