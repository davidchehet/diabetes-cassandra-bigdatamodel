from ..config import get_session
from ..utils import get_query_by_tag
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report
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
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# Random forest model
rf_model = RandomForestClassifier(class_weight='balanced', max_depth=5, min_samples_split=5, n_estimators=50, min_samples_leaf=1, random_state=42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)
report_rf = classification_report(y_test, y_pred_rf, output_dict=True)

# KNN model
knn_model = KNeighborsClassifier(n_neighbors=5)
knn_model.fit(X_train_scaled, y_train)
y_pred_knn = knn_model.predict(X_test_scaled)
report_knn = classification_report(y_test, y_pred_knn, output_dict=True)

# GNB model
gnb_model = GaussianNB()
gnb_model.fit(X_train_scaled, y_train)
y_pred_gnb = gnb_model.predict(X_test_scaled)
report_gnb = classification_report(y_test, y_pred_gnb, output_dict=True)

# Compile metrics
metrics = {
    'Random Forest': {'precision': report_rf['1']['precision'], 'recall': report_rf['1']['recall'], 'f1-score': report_rf['1']['f1-score']},
    'KNN': {'precision': report_knn['1']['precision'], 'recall': report_knn['1']['recall'], 'f1-score': report_knn['1']['f1-score']},
    'Gaussian NB': {'precision': report_gnb['1']['precision'], 'recall': report_gnb['1']['recall'], 'f1-score': report_gnb['1']['f1-score']}
}

metrics_df = pd.DataFrame.from_dict(metrics, orient='index')

# Create the visualization
metrics_df.plot(kind='bar', figsize=(10, 6), rot=0)
plt.title('Comparison of Precision, Recall, and F1-Score for ML Models (Diabetes Class)')
plt.ylabel('Score')
plt.xlabel('Model')
plt.legend(title='Metric')
plt.grid(axis='y')
plt.tight_layout()
plt.show()

session.shutdown()