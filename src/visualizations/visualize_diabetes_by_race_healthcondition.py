from ..config import get_session
from ..utils import get_query_by_tag
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

session = get_session()
if session:
    print('Connected!')
else:
    print('Error occurred')

# Query our gold table
rows = session.execute(get_query_by_tag('src/cql_scripts/gold_scripts.cql', 'SELECT_FROM_NEW_GOLD_TABLE_RACE_HEALTHCONDITION'))

# Make a dataframe to use in our visualization tools
df = pd.DataFrame(list(rows))

plt.figure(figsize=(12,  7))
sns.barplot(x='race', y='diabetes_prevalence', hue='condition_group', data=df, palette='viridis')
plt.title('Prevalence of Diabetes by Race and Co-existing Health Conditions')
plt.xlabel('Race')
plt.ylabel('Proportion with Diabetes')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Condition Group')
plt.tight_layout()
plt.show()

session.shutdown()