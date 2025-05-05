from ..config import get_session
from ..utils import get_query_by_tag
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt 

session = get_session()
if session:
    print('Connected!')
else:
    print('Error occurred')

get_numeric_data = get_query_by_tag('src/cql_scripts/silver_scripts.cql', 'RANDOM_FOREST')

rows = session.execute(get_numeric_data)
df = pd.DataFrame(list(rows))

# X = features, y = label
X = df.drop('diabetes', axis=1)
y = df['diabetes']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Best Recall Model
model = RandomForestClassifier(class_weight='balanced', max_depth=5, min_samples_split=5, n_estimators=50, min_samples_leaf=1, random_state=42)

# Best F1 Model
#model = RandomForestClassifier(class_weight={0: 1, 1: 2}, max_depth=15, min_samples_split=10, n_estimators=100, random_state=42)

model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate model performance
accuracy = accuracy_score(y_test, y_pred)

'''
# GridSearch CV
param_grid = {
    'n_estimators': [10, 50, 100],
    'max_depth': [None, 5, 10, 15],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 3, 5],
    'class_weight': ['balanced', {0: 1, 1: 2}, {0: 1, 1: 5}]
}

grid_search = GridSearchCV(estimator=model, param_grid=param_grid, scoring='f1', cv=3, n_jobs=-1)
grid_search.fit(X_train, y_train)
print("Best accuracy: ", grid_search.best_score_)
print(grid_search.best_estimator_)
print("Best parameters found: ", grid_search.best_params_)
print("Best recall score: ", grid_search.best_score_)

'''

# Make sure I am not overfitting
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='accuracy')

print("Cross-validation Accuracy Scores:", cv_scores)
print("Mean CV Accuracy:", cv_scores.mean())

print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print(f"Accuracy: {accuracy}")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()


session.shutdown()


