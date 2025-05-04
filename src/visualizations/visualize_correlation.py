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

# Get numerical and diabetes data from silver
rows = session.execute(get_query_by_tag('src/cql_scripts/silver_scripts.cql', 'SELECT_VIS_THREE'))

# DF logic
df = pd.DataFrame(list(rows))

# Separate data for correlation between diabetes status
diabetes_positive = df[df['diabetes'] == 1][['age', 'bmi', 'hba1c_level', 'blood_glucose_level']]
diabetes_negative = df[df['diabetes'] == 0][['age', 'bmi', 'hba1c_level', 'blood_glucose_level']]

# Correlation matrices
corr_pos = diabetes_positive.corr()
corr_neg = diabetes_negative.corr()

# Heatmap
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

sns.heatmap(corr_neg, annot=True, cmap='coolwarm', fmt='.2f', ax=axes[0])
axes[0].set_title('Correlation Matrix Diabetes Negative')

sns.heatmap(corr_pos, annot=True, cmap='coolwarm', fmt='.2f', ax=axes[1])
axes[1].set_title('Correlation Matrix Diabetes Positive')

plt.tight_layout()
plt.show()

session.shutdown()


