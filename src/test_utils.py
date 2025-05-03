from utils import get_query_by_tag
from utils import binarize_gender
from utils import format_location
from utils import categorize_smoking_history
import pandas as pd

filename = 'src/cql_scripts/bronze_scripts.cql'
tag = 'CREATE_BRONZE_LEVEL_TABLE'
get_query_by_tag(filename, tag)

df = pd.read_csv('./diabetes.csv')
df['gender'].unique() # <== ['Female', 'Male', 'Other']
df['gender'].value_counts() # <== Female 58.5k, Male 41.4k, Other 18

binarize_gender('Female')
binarize_gender('Male')
binarize_gender('Other')

null_counts = df.isnull().sum()
null_counts # <== No null values in this dataset

format_location('alabAMa')

df['smoking_history'].unique()
df['smoking_history'].value_counts()
categorize_smoking_history('never')
categorize_smoking_history('ever')
categorize_smoking_history('not current')
categorize_smoking_history('former')
categorize_smoking_history('current')
categorize_smoking_history('No Info')

bmi_stats = df['bmi'].describe().apply(lambda x: format(x, 'f'))
hba1c_stats = df['hbA1c_level'].describe().apply(lambda x: format(x, 'f'))
blood_glucose_stats = df['blood_glucose_level'].describe().apply(lambda x: format(x, 'f'))
age_stats = df['age'].describe().apply(lambda x : format (x, 'f'))

print(age_stats)


