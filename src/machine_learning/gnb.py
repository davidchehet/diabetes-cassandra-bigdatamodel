from ..config import get_session
from ..utils import get_query_by_tag
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

session = get_session()
if session:
    print('Connected!')
else:
    print('Error occurred')

get_numeric_data = get_query_by_tag('src/cql_scripts/silver_scripts.cql', 'ML_QUERY')

rows = session.execute(get_numeric_data)
df = pd.DataFrame(list(rows))

# X = features, y = label
X = df.drop('diabetes', axis=1)
y = df['diabetes']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Scaling
scaler = StandardScaler()
X_trained_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = GaussianNB()
model.fit(X_trained_scaled, y_train)

y_pred = model.predict(X_test_scaled)

accuracy = accuracy_score(y_test, y_pred)

print("Accuracy: ", accuracy)
print("Classification report:")
print(classification_report(y_test, y_pred))

# Confusion Matrix
cm_knn = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm_knn, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted (GNB)')
plt.ylabel('Actual')
plt.title('GNB Confusion Matrix')
plt.show()

session.shutdown()